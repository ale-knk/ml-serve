FROM python:3.11-slim

WORKDIR /training

# Dependencias de sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar requirements y proyecto entero
COPY infra/train/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . .

# Comando por defecto (puede ser sobreescrito desde docker-compose)
CMD ["python", "-m", "model.train"]
