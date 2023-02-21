.PHONY: default
default:
	@echo Choose target: run, venv


.PHONY: run
run:
	./venv/Scripts/python.exe -m emi

.PHONY: venv
venv:
	python -m venv venv
	./venv/Scripts/python.exe -m pip install --upgrade pip setuptools wheel
	./venv/Scripts/python.exe -m pip install -r ./requirements.txt
