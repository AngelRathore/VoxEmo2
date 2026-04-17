.PHONY: install dev backend frontend health clean

install:
	cd backend && python -m venv venv && \
	  . venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install

dev:
	@echo "Starting backend + frontend..."
	make -j2 backend frontend

backend:
	cd backend && . venv/bin/activate && uvicorn main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

health:
	curl -s http://localhost:8000/health | python3 -m json.tool

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -f backend/voxemo.db