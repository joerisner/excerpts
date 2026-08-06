.DEFAULT_GOAL=help
.PHONY: help clean setup ci

ci: ## Run CI locally
	@bin/ci

clean: ## Remove temporary artifacts
	@bin/clean

setup: ## Install uv, required Python version, and Git pre-push hook to run CI locally
	@bin/setup

help:  ## Show this help
	@awk 'BEGIN {FS = ":.*##"; \
	printf "\nCommands:\n\033[35m\033[0m"} /^[$$()% a-zA-Z_-]+:.*?##/ { \
	printf "  \033[35;1m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { \
	printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
