PROJECT_NAME=airflow
DAG_ID=macro_data_ingestion
COMPOSE = $(shell command -v docker-compose >/dev/null 2>&1 && echo docker-compose || echo docker compose)

.PHONY: init up down logs restart rebuild trigger bash

init:
	# Create folders that should exist at runtime
	mkdir -p logs plugins
	chmod -R 755 logs plugins

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

restart:
	$(COMPOSE) down -v
	$(COMPOSE) up --build

rebuild:
	$(COMPOSE) down -v
	$(COMPOSE) build
	$(COMPOSE) up airflow-init
	$(COMPOSE) up -d airflow-webserver airflow-scheduler

trigger:
	$(COMPOSE) exec airflow-webserver airflow dags trigger $(DAG_ID)	

bash:
	$(COMPOSE) exec airflow-webserver bash