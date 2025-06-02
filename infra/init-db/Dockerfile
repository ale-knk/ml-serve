FROM python:3.11-slim

RUN apt-get update && apt-get install -y postgresql-client && \
    pip install --no-cache-dir psycopg2-binary

COPY infra/init-db/entrypoint.sh /entrypoint.sh
COPY infra/init-db/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ../.. /app
WORKDIR /app

ENTRYPOINT ["sh", "/entrypoint.sh"]
