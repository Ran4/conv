test: .venv
	pytest conv.py -v

.venv:
	python3 -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt
