PROJECT_NAME=mlserve
COMPOSE=docker compose -f infrastructure/docker-compose.yml --project-name $(PROJECT_NAME)

# Levanta solo infraestructura: API, DB y MLflow (NO training)
up:
	set -a; . .env; set +a; \
	docker compose -f infrastructure/docker-compose.yml --project-name $(PROJECT_NAME) up api postgres minio minio-create-bucket mlflow --build

down:
	set -a; . .env; set +a; \
	docker compose -f infrastructure/docker-compose.yml --project-name $(PROJECT_NAME) down -v


# Lanza entrenamiento puntual (run + destroy)
train:
	set -a; . .env; set +a; \
	docker compose -f infrastructure/docker-compose.yml --project-name $(PROJECT_NAME) run --rm --no-deps training

# Logs en tiempo real
logs:
	$(COMPOSE) logs -f

# Lista de contenedores activos
ps:
	$(COMPOSE) ps

# Construye todas las imágenes (por si quieres forzar build sin levantar)
build:
	$(COMPOSE) build

