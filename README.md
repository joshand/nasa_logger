# NASA Image Downloader (for EPIC images)

Small Flask app that fetches NASA Image metadata and stores it in SQLite.
Focus areas:
- Structured JSON logging via **structlog**
- Requests with retries & latency timing
- Clean config with **pydantic** + `.env`
- SQLAlchemy 2.0 models + upsert
- Unit tests with mocking
- Minimal HTML view

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add NASA_API_KEY (or leave DEMO_KEY)
python -m src.app
