run:
	uvicorn app.main:app --port 8080 --log-level info --timeout-keep-alive 30

run-debug:
	uvicorn app.main:app --reload --port 8080 --log-level debug --timeout-keep-alive 30