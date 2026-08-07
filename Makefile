COMPOSE = docker compose -f deploy/docker-compose.yaml --env-file .env
COMPOSE_MONITORING = docker compose -f monitoring/docker-compose.yaml --env-file .env

.PHONY: \
	up stop down logs rebuild \
	up-db stop-db down-db logs-db \
	up-n8n stop-n8n down-n8n logs-n8n

# ========================
# Application
# ========================

up:
	$(COMPOSE) --profile app up -d

stop:
	$(COMPOSE) --profile app stop

down:
	$(COMPOSE) --profile app down --rmi local

logs:
	$(COMPOSE) logs -f --tail 1000

rebuild: down up


# ========================
# Infrastructure
# ========================

up-db:
	$(COMPOSE) up -d

stop-db:
	$(COMPOSE) stop

down-db:
	$(COMPOSE) down --rmi local

logs-db:
	$(COMPOSE) logs -f --tail 1000

rebuild: down-db up-db