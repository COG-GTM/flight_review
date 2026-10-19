# Base pinned by digest (CM-2 / SR-4(3)); the tag is kept for readability only.
# ubuntu:noble (24.04 LTS) as recorded in sbom/GENERATION_RECORD.md.
ARG BASE_IMAGE=ubuntu:noble@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac
FROM ${BASE_IMAGE}

COPY requirements.txt requirements.txt

RUN apt-get	update && \
	apt-get install -y --no-install-recommends apt-utils python3 python3-pip sqlite3 libfftw3-bin python3-setuptools && \
	apt-get install -y --no-install-recommends python3-dev libfftw3-dev git && \
	pip3 install --break-system-packages --no-cache-dir -r requirements.txt && \
	apt-get remove -y python3-dev libfftw3-dev git && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

# Unprivileged runtime identity (AC-6 / CM-7). UID/GID 10001 is outside the
# host's normal user range so a bind-mounted volume is never accidentally
# writable by a real host account.
RUN groupadd --system --gid 10001 flightreview && \
	useradd --system --uid 10001 --gid 10001 --no-create-home --home-dir /opt/service --shell /usr/sbin/nologin flightreview

RUN mkdir -p /opt/service/data /opt/data
COPY --chown=10001:10001 [".", "/opt/service/"]
RUN chown -R 10001:10001 /opt/service /opt/data

WORKDIR /opt/service
ENV HOME=/tmp
USER 10001:10001
EXPOSE 5006
CMD ["/opt/service/run.sh"]

## USAGE
## ## ## ## ## ## ## ## ## ## ## ## 
## BUILD  docker build -t px4flightreview -f docker/Dockerfile .
## RUN    docker run -d -p 5006:5006 -v /<full_path>/config_user.ini:/opt/service/config_user.ini px4flightreview
## The container runs as UID 10001; a bind-mounted ./data directory must be
## writable by that UID (e.g. `sudo chown -R 10001:10001 data`).
