"""
Minimal synthetic ULog generator for tests.

Writes a valid ULog file (header, flag bits, format/info/parameter
definitions, subscriptions and data messages) from numpy arrays so that
pyulog can read it back. pyulog's ULog.write_ulog() only re-serializes a
parsed log, so the raw format is written directly here.
"""
import struct

import numpy as np

HEADER_BYTES = b'\x55\x4c\x6f\x67\x01\x12\x35'
MSG_TYPE_FORMAT = ord('F')
MSG_TYPE_DATA = ord('D')
MSG_TYPE_INFO = ord('I')
MSG_TYPE_PARAMETER = ord('P')
MSG_TYPE_ADD_LOGGED_MSG = ord('A')
MSG_TYPE_FLAG_BITS = ord('B')

STANDARD_GRAVITY = 9.80665

# ULog type name -> struct format
_STRUCT_TYPES = {
    'uint8_t': 'B', 'int8_t': 'b', 'uint16_t': 'H', 'int16_t': 'h',
    'uint32_t': 'I', 'int32_t': 'i', 'uint64_t': 'Q', 'int64_t': 'q',
    'float': 'f', 'double': 'd', 'bool': '?',
}


def _msg(msg_type, payload):
    return struct.pack('<HB', len(payload), msg_type) + payload


def _format_msg(name, fields):
    """ fields: list of (type_str, array_size, field_name) """
    text = name + ':'
    for type_str, array_size, field_name in fields:
        if array_size > 1:
            text += '{}[{}] {};'.format(type_str, array_size, field_name)
        else:
            text += '{} {};'.format(type_str, field_name)
    return _msg(MSG_TYPE_FORMAT, text.encode('utf-8'))


def _info_msg(key, value):
    key_bytes = 'char[{}] {}'.format(len(value), key).encode('utf-8')
    return _msg(MSG_TYPE_INFO, struct.pack('<B', len(key_bytes)) + key_bytes
                + value.encode('utf-8'))


def _param_msg(name, value):
    key_bytes = 'float {}'.format(name).encode('utf-8')
    return _msg(MSG_TYPE_PARAMETER, struct.pack('<B', len(key_bytes)) + key_bytes
                + struct.pack('<f', value))


def _struct_format(fields):
    fmt = '<'
    for type_str, array_size, _ in fields:
        fmt += _STRUCT_TYPES[type_str] * array_size
    return fmt


class Topic:
    """ one logged topic: format definition plus column arrays """

    def __init__(self, name, fields, columns):
        """
        :param fields: list of (type_str, array_size, field_name); the first
            field must be ('uint64_t', 1, 'timestamp')
        :param columns: dict field_name -> array (or list of arrays for array fields)
        """
        self.name = name
        self.fields = fields
        self.columns = columns

    def data_messages(self, msg_id):
        fmt = _struct_format(self.fields)
        num_samples = len(self.columns['timestamp'])
        messages = []
        for i in range(num_samples):
            values = []
            for type_str, array_size, field_name in self.fields:
                column = self.columns[field_name]
                if array_size > 1:
                    values.extend(_cast(type_str, column[j][i]) for j in range(array_size))
                else:
                    values.append(_cast(type_str, column[i]))
            payload = struct.pack('<H', msg_id) + struct.pack(fmt, *values)
            messages.append((int(self.columns['timestamp'][i]), _msg(MSG_TYPE_DATA, payload)))
        return messages


def _cast(type_str, value):
    if type_str == 'bool':
        return bool(value)
    if type_str in ('float', 'double'):
        return float(value)
    return int(value)


def write_ulog(filename, topics, start_timestamp_us, sys_name='PX4'):
    """ write topics (list of Topic) to a ULog file """
    out = bytearray()
    out += HEADER_BYTES + struct.pack('B', 1) + struct.pack('<Q', start_timestamp_us)
    out += _msg(MSG_TYPE_FLAG_BITS, bytes(8) + bytes(8) + struct.pack('<QQQ', 0, 0, 0))
    for topic in topics:
        out += _format_msg(topic.name, topic.fields)
    out += _info_msg('sys_name', sys_name)
    out += _info_msg('ver_hw', 'SYNTHETIC')
    out += _info_msg('ver_sw', '0.0.0')
    out += _param_msg('SYS_AUTOSTART', 2100.0)
    out += _param_msg('MAV_TYPE', 1.0)

    data = []
    for msg_id, topic in enumerate(topics):
        payload = struct.pack('<BH', 0, msg_id) + topic.name.encode('utf-8')
        out += _msg(MSG_TYPE_ADD_LOGGED_MSG, payload)
        data.extend(topic.data_messages(msg_id))
    data.sort(key=lambda item: item[0])
    for _, message in data:
        out += message

    with open(filename, 'wb') as ulog_file:
        ulog_file.write(bytes(out))


def _quaternion_from_roll(roll_rad):
    """ attitude quaternion (w, x, y, z) for a pure roll angle """
    half = roll_rad / 2.0
    return np.cos(half), np.sin(half), np.zeros_like(half), np.zeros_like(half)


def synthetic_flight(filename, duration_s=120.0, rate_hz=20.0, start_timestamp_us=1_000_000,
                     include=('vehicle_acceleration', 'airspeed_validated',
                              'vehicle_local_position', 'vehicle_attitude'),
                     nz_bust=(50.0, 55.0, 3.2), invalid_z=(100.0, 110.0), with_vz=True,
                     ref_alt=0.0, ref_alt_valid_from_s=0.0, airspeed_invalid=None):
    """
    Write a synthetic fixed-wing flight:

    * level flight at 1 g, with an Nz pull of `nz_bust[2]` g between
      nz_bust[0] and nz_bust[1] seconds
    * airspeed ramps 15 -> 35 m/s over the flight
    * altitude climbs 100 m -> 220 m then descends, with z/v_z marked
      invalid in the `invalid_z` window
    * a 45 degree bank between 70 s and 80 s
    * `with_vz=False` omits the vz / v_z_valid fields from vehicle_local_position
    * `ref_alt` (m AMSL) is NaN before `ref_alt_valid_from_s` seconds
    * `airspeed_invalid=(t0, t1)` marks selected_airspeed_index = -1 in that window

    :return: dict with the ground-truth arrays (time_s, nz_g, airspeed, alt_m, vz, bank_deg)
    """
    num = int(duration_s * rate_hz) + 1
    time_s = np.linspace(0.0, duration_s, num)
    timestamps = (start_timestamp_us + time_s * 1e6).astype(np.uint64)

    nz_g = np.ones(num)
    bust_mask = (time_s >= nz_bust[0]) & (time_s < nz_bust[1])
    nz_g[bust_mask] = nz_bust[2]

    airspeed = 15.0 + 20.0 * time_s / duration_s

    alt_m = np.where(time_s < duration_s / 2,
                     100.0 + 120.0 * time_s / (duration_s / 2),
                     220.0 - 120.0 * (time_s - duration_s / 2) / (duration_s / 2))
    vz = np.gradient(-alt_m, time_s)  # positive down
    z_valid = ~((time_s >= invalid_z[0]) & (time_s < invalid_z[1]))

    airspeed_index = np.ones(num, dtype=np.int8)
    if airspeed_invalid is not None:
        airspeed_index[(time_s >= airspeed_invalid[0]) & (time_s < airspeed_invalid[1])] = -1

    ref_alt_column = np.full(num, float(ref_alt))
    ref_alt_column[time_s < ref_alt_valid_from_s] = np.nan

    bank_rad = np.zeros(num)
    bank_rad[(time_s >= 70.0) & (time_s < 80.0)] = np.radians(45.0)
    q_w, q_x, q_y, q_z = _quaternion_from_roll(bank_rad)

    topics = []
    if 'vehicle_acceleration' in include:
        topics.append(Topic('vehicle_acceleration', [
            ('uint64_t', 1, 'timestamp'), ('uint64_t', 1, 'timestamp_sample'),
            ('float', 3, 'xyz')], {
                'timestamp': timestamps, 'timestamp_sample': timestamps,
                'xyz': [np.zeros(num), np.zeros(num), -nz_g * STANDARD_GRAVITY]}))
    if 'airspeed_validated' in include:
        topics.append(Topic('airspeed_validated', [
            ('uint64_t', 1, 'timestamp'), ('float', 1, 'indicated_airspeed_m_s'),
            ('float', 1, 'calibrated_airspeed_m_s'), ('float', 1, 'true_airspeed_m_s'),
            ('bool', 1, 'airspeed_sensor_measurement_valid'),
            ('int8_t', 1, 'selected_airspeed_index')], {
                'timestamp': timestamps, 'indicated_airspeed_m_s': airspeed,
                'calibrated_airspeed_m_s': airspeed, 'true_airspeed_m_s': airspeed * 1.05,
                'airspeed_sensor_measurement_valid': np.ones(num, dtype=bool),
                'selected_airspeed_index': airspeed_index}))
    if 'vehicle_local_position' in include:
        fields = [('uint64_t', 1, 'timestamp'), ('float', 1, 'x'), ('float', 1, 'y'),
                  ('float', 1, 'z'), ('float', 1, 'vx'), ('float', 1, 'vy'),
                  ('float', 1, 'ref_alt'), ('bool', 1, 'xy_valid'), ('bool', 1, 'z_valid'),
                  ('bool', 1, 'v_xy_valid')]
        columns = {'timestamp': timestamps, 'x': airspeed * time_s, 'y': np.zeros(num),
                   'z': -alt_m, 'vx': airspeed, 'vy': np.zeros(num),
                   'ref_alt': ref_alt_column, 'xy_valid': np.ones(num, dtype=bool),
                   'z_valid': z_valid, 'v_xy_valid': np.ones(num, dtype=bool)}
        if with_vz:
            fields += [('float', 1, 'vz'), ('bool', 1, 'v_z_valid')]
            columns.update({'vz': vz, 'v_z_valid': z_valid})
        topics.append(Topic('vehicle_local_position', fields, columns))
    if 'vehicle_air_data' in include:
        topics.append(Topic('vehicle_air_data', [
            ('uint64_t', 1, 'timestamp'), ('float', 1, 'baro_alt_meter'),
            ('float', 1, 'baro_temp_celcius'), ('float', 1, 'baro_pressure_pa')], {
                'timestamp': timestamps, 'baro_alt_meter': alt_m,
                'baro_temp_celcius': np.full(num, 20.0),
                'baro_pressure_pa': np.full(num, 101325.0)}))
    if 'vehicle_attitude' in include:
        topics.append(Topic('vehicle_attitude', [
            ('uint64_t', 1, 'timestamp'), ('float', 4, 'q')], {
                'timestamp': timestamps, 'q': [q_w, q_x, q_y, q_z]}))

    write_ulog(filename, topics, start_timestamp_us)
    return {'time_s': time_s, 'nz_g': nz_g, 'airspeed': airspeed, 'alt_m': alt_m,
            'vz': vz, 'bank_deg': np.degrees(bank_rad), 'z_valid': z_valid}


if __name__ == '__main__':
    import sys
    synthetic_flight(sys.argv[1] if len(sys.argv) > 1 else 'synthetic_flight.ulg')
