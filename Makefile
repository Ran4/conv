test: .venv
	. .venv/bin/activate && pytest conv.py -v

.venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
