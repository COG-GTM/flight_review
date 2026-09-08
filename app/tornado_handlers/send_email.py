""" Methods for sending notification emails """
from __future__ import print_function

import sys
import os

from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol
                                           # (port 465, uses SSL)
# from smtplib import SMTP                  # use this for standard SMTP protocol
                                           # (port 25, no encryption)
from email.mime.text import MIMEText

# this is needed for the following imports
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plot_app'))
from config import *
from helper import is_valid_email
from security import sanitize_header_value


def send_notification_email(email_address, plot_url, delete_url, info):
    """ send a notification email after uploading a plot
        :param info: dictionary with additional info
    """

    if not is_valid_email(email_address):
        return True

    description = info['description']
    if description == '':
        description = info['airframe']
        if 'vehicle_name' in info:
            description = "{:} - {:}".format(description, info['vehicle_name'])

    subject = "Log File uploaded ({:})".format(description)
    destination = [email_address]

    content = """\
Hi there!

Your uploaded log file is available under:
{plot_url}

Description: {description}
Feedback: {feedback}
Vehicle type: {type}
Airframe: {airframe}
Hardware: {hardware}
Vehicle UUID: {uuid}
Software git hash: {software}
Upload file name: {upload_filename}

Use the following link to delete the log:
{delete_url}
""".format(plot_url=plot_url, delete_url=delete_url, **info)

    return _send_email(destination, subject, content)


def send_flightreport_email(destination, plot_url, rating_description,
                            wind_speed, delete_url, uploader_email, info):
    """ send notification email for a flight report upload """

    if len(destination) == 0:
        return True

    content = """\
Hi

A new flight report just got uploaded:
{plot_url}

Description: {description}
Feedback: {feedback}

Vehicle type: {type}
Airframe: {airframe}
Hardware: {hardware}
Vehicle UUID: {uuid}
Software git hash: {software}

Use the following link to delete the log:
{delete_url}
""".format(plot_url=plot_url,
           rating_description=rating_description, wind_speed=wind_speed,
           delete_url=delete_url, uploader_email=uploader_email, **info)

    description = info['description']
    if description == '':
        description = info['airframe']
        if 'vehicle_name' in info:
            description = "{:} - {:}".format(description, info['vehicle_name'])

    subject = "Flight Report uploaded ({:})".format(description)
    if info['rating'] == 'crash_sw_hw':
        subject = '[CRASH] '+subject

    return _send_email(destination, subject, content)


def _send_email(destination, subject, content):
    """ common method for sending an email to one or more destinations.
    Header values are sanitized (no CR/LF, length-limited) and every
    destination must be a syntactically valid address. """

    destination = [addr for addr in destination if is_valid_email(addr)]
    if len(destination) == 0:
        return False

    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = sanitize_header_value(subject)
        sender = email_config['sender']
        msg['From'] = sender # some SMTP servers will do this automatically

        conn = SMTP(email_config['smtpserver'], timeout=15)
        conn.set_debuglevel(False)
        conn.login(email_config['user_name'], email_config['password'])
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()

    except Exception as exc:
        print("mail failed; {:}".format(str(exc)))
        return False
    return True
