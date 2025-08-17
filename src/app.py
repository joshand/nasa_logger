from flask import Flask, render_template, redirect, url_for, request, flash
from src.db import init_db, SessionLocal
from src.models import Image
from src.services.ingest import ingest_apod, ingest_epic
from src.logging_setup import configure_logging, logger


def create_app() -> Flask:
    configure_logging()
    app = Flask(__name__)
    app.secret_key = "dev-secret"  # replace for production
    init_db()

    @app.get("/")
    def index():
        with SessionLocal() as session:
            entries = session.query(Image).order_by(Image.date.desc()).limit(30).all()
        return render_template("index.html", entries=entries)

    @app.post("/fetch")
    def fetch():
        date = request.form.get("date") or None
        try:
            ingest_epic(date)
            flash("Fetched Image successfully", "success")
            logger.info("manual_fetch_success", date=date)
        except Exception as e:
            flash(f"Fetch failed: {e}", "danger")
            logger.error("manual_fetch_error", date=date, error=str(e))
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
