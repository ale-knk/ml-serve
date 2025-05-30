PROJECT_NAME=mlserve
include .env
export $(shell sed 's/=.*//' .env)

up:
	set -a; . .env; set +a;
	docker compose -f infrastructure/docker-compose.yml -p $(PROJECT_NAME) up --build -d postgres minio
	docker compose -f infrastructure/docker-compose.yml -p $(PROJECT_NAME) up --build -d minio-create-bucket
	docker compose -f infrastructure/docker-compose.yml -p $(PROJECT_NAME) up --build -d mlflow pgadmin
	docker compose -f infrastructure/docker-compose.yml -p $(PROJECT_NAME) up --build -d init-db
	docker compose -f infrastructure/docker-compose.yml -p $(PROJECT_NAME) up --build -d api
	docker compose -f infrastructure/docker-compose.yml -p $(PROJECT_NAME) up --build -d training

down:
	set -a; . .env; set +a; \
	docker compose -f infrastructure/docker-compose.yml --project-name $(PROJECT_NAME) down -v

train:
	set -a; . .env; set +a; \
	docker compose -f infrastructure/docker-compose.yml --project-name $(PROJECT_NAME) build training && \
	docker compose -f infrastructure/docker-compose.yml --project-name $(PROJECT_NAME) run --rm --no-deps training

