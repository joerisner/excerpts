.DEFAULT_GOAL=help
.PHONY: help clean setup dev ci tf-plan tf-apply tf-fmt

ci: ## Run CI locally
	@bin/ci

clean: ## Remove temporary artifacts
	@bin/clean

coverage: ## View test coverage report in browser
	@open tests/coverage/html/index.html

setup: ## Install uv, required Python version, and Git pre-push hook to run CI locally
	@bin/setup

dev: setup ## Run the application in dev mode
	@uv run fastapi dev --port 3000

test: ## Run test suite
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
