.PHONY: help clean deploy test format
.DEFAULT_GOAL := help

PACKAGE_DIR := package
STAGE := dev

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help: ## display help information
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: ## remove Python artifacts
	@$(MAKE) -C ouroboros clean

deploy: ## deploy AWS Lambda function via Serverless
	serverless deploy -v --stage ${STAGE}

test: ## run ouroboros tests
	@$(MAKE) -C ouroboros test

format: ## format ouroboros code and imports
	@$(MAKE) -C ouroboros format
