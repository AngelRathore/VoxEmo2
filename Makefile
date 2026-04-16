.PHONY: install dev backend frontend clean help

# ── Setup ──────────────────────────────────────────────
install:        ## Install all dependencies (Python venv + npm)
	@echo "📦 Setting up Python venv..."
	cd backend && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "📦 Installing frontend packages..."
	cd frontend && npm install
	@echo "📦 Installing root dev tools..."
	npm install
	@echo "✅ All done!"

# ── Dev ────────────────────────────────────────────────
dev:            ## Start both backend and frontend (requires concurrently)
	npm run dev

backend:        ## Start only the FastAPI backend
	cd backend && . venv/bin/activate && uvicorn app.main:app --reload --port 8000

frontend:       ## Start only the React frontend
	cd frontend && npm start

# ── Checks ─────────────────────────────────────────────
health:         ## Check if the API is running
	@curl -s http://localhost:8000/health | python -m json.tool || echo "❌ Backend not running"

models:         ## List model files in backend/models/
	@ls -lh backend/models/ || echo "No models directory found"

# ── Clean ──────────────────────────────────────────────
clean:          ## Remove venv, node_modules, build artifacts
	rm -rf backend/venv
	rm -rf frontend/node_modules
	rm -rf frontend/build
	rm -rf node_modules
	@echo "🧹 Cleaned!"

# ── Help ───────────────────────────────────────────────
help:           ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
