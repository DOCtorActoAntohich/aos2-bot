.PHONY: format
format:
	black ./emi/ && ruff --fix ./emi/

.PHONY: lint
lint:
	black --check ./emi/ && ruff ./emi/ && mypy --install-types --non-interactive ./emi/
