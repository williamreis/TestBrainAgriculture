.PHONY: help setup run stop migrate test test-coverage test-unit test-integration logs clean seed seed-force

help: ## Mostra esta ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Configurar o projeto (instalar dependências, inicializar Alembic)
	@echo "Configurando o projeto..."
	docker compose up -d --build
	docker compose exec api uv run alembic upgrade head
	@echo "Projeto configurado!"

run: ## Subir os containers
	docker compose up -d

stop: ## Parar os containers
	docker compose down

migrate: ## Executar migrações
	docker compose exec api uv run alembic upgrade head

migrate-create: ## Criar nova migração (use: make migrate-create name=nome_da_migracao)
	docker compose exec api uv run alembic revision --autogenerate -m "$(name)"

test: ## Rodar testes
	docker compose exec api uv run pytest -v

test-coverage: ## Rodar testes com cobertura
	docker compose exec api uv run pytest --cov=app --cov-report=html

test-unit: ## Rodar apenas testes unitários
	docker compose exec api uv run pytest app/tests/ -v -k "not integration"

test-integration: ## Rodar apenas testes de integração
	docker compose exec api uv run pytest app/tests/ -v -k "integration"

seed: ## Popular banco com dados mockados (Faker)
	@echo "Populando banco com dados mockados..."
	docker compose exec api uv run python -m app.utils.seed_data

seed-force: ## Forçar população do banco (apaga dados existentes)
	@echo "Forçando população do banco com dados mockados..."
	docker compose exec api uv run python -m app.utils.seed_data --force

logs: ## Ver logs dos containers
	docker compose logs -f

clean: ## Limpar containers e volumes
	docker compose down -v
	docker system prune -f

shell: ## Acessar shell do container da API
	docker compose exec api bash

db-shell: ## Acessar shell do banco de dados
	docker compose exec db psql -U postgres -d brainagriculture

dashboard: ## Rodar apenas o dashboard Streamlit
	docker compose up dashboard

api-only: ## Rodar apenas a API (sem dashboard)
	docker compose up db api
