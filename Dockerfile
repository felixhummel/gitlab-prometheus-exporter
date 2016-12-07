FROM python:3-alpine

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY gitlab_exporter.py /usr/local/bin/
EXPOSE 3001

RUN adduser -S monitor

VOLUME /home/monitor/.python-gitlab.cfg
USER monitor
CMD /usr/local/bin/gitlab_exporter.py
