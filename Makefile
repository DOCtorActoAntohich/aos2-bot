.PHONY: format
format:
	black ./src/ && ruff --fix ./src/

.PHONY: lint
lint:
	black --check ./src/ && ruff ./src/ && mypy --install-types --non-interactive ./src/
