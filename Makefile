.DEFAULT_GOAL=help
.PHONY: ci clean coverage db-migrate db-start db-stop dev setup stop test tf-plan tf-apply tf-fmt help

ci: ## Run CI locally
	@bin/ci

clean: ## Remove temporary artifacts
	@bin/clean

coverage: ## View test coverage report in browser
	@open tests/coverage/html/index.html

db-migrate: ## Run database migrations
	@uv run alembic upgrade head

db-start: ## Start dev and test database containers
	@open -a Docker && while (! docker stats --no-stream &> /dev/null ); do sleep 1; done
	@printf "\033[34;1m== Starting postgres container ==\033[0m\n"
	@docker compose up -d
	@echo ""
	@sleep 1

db-stop: ## Stop running database containers
	@docker compose down

dev: setup db-start ## Run the application in dev mode
	@uv run fastapi dev --port 3000

setup: ## Setup the local environment for development
	@bin/setup

test: setup db-start ## Run test suite
	@uv run pytest

# Terraform
tf-plan: ## Run terraform plan
	@terraform -chdir=infra init
	@terraform -chdir=infra plan

tf-apply: ## Run terraform apply
	@terraform -chdir=infra apply

tf-fmt: ## Format terraform config
	@terraform -chdir=infra fmt

help:  ## Show this help
	@awk 'BEGIN {FS = ":.*##"; \
	printf "\nCommands:\n\033[35m\033[0m"} /^[$$()% a-zA-Z_-]+:.*?##/ { \
	printf "  \033[35;1m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { \
	printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
