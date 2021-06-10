FROM python:3.9.5-alpine

WORKDIR /mnt
ENV GITCHANGELOG_CONFIG_FILENAME /usr/local/etc/gitchangelog.rc

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt --no-cache-dir \
  && apk add --no-cache git=2.30.2-r0

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY .gitchangelog.rc /usr/local/etc/gitchangelog.rc

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
