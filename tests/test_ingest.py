from unittest.mock import patch


def test_ingest_insert_and_update():
    from src.services.ingest import ingest_apod
    from src.models import Image
    from src.db import SessionLocal

    with patch("src.services.ingest.fetch_apod") as mock_fetch:
        mock_fetch.return_value = {
            "date": "2025-08-16", "title": "Title1",
            "media_type": "image", "url": "https://x",
        }
        ingest_apod()

    # Assert using a fresh session
    with SessionLocal() as s:
        row = s.query(Image).first()
        assert row.title == "Title1"
