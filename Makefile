test: .venv
	. .venv/bin/activate && pytest -v

.venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
