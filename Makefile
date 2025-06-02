PROJECT_NAME=mlserve
include .env
export $(shell sed 's/=.*//' .env)

up:
	set -a; . .env; set +a;
	docker compose -f infra/docker-compose.yml -p $(PROJECT_NAME) up --build -d

down:
	set -a; . .env; set +a; \
	docker compose -f infra/docker-compose.yml --project-name $(PROJECT_NAME) down -v

train:
	set -a; . .env; set +a; \
	docker compose -f infra/docker-compose.yml --project-name $(PROJECT_NAME) build training && \
	docker compose -f infra/docker-compose.yml --project-name $(PROJECT_NAME) run --rm --no-deps training

