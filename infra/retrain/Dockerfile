FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y cron curl && \
    apt-get clean

WORKDIR /app

COPY infra/retrain/cronjob /etc/cron.d/retrain-cron
COPY infra/retrain/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN chmod 0644 /etc/cron.d/retrain-cron && \
    crontab /etc/cron.d/retrain-cron && \
    touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
