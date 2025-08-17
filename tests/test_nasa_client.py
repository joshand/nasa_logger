from unittest.mock import patch


def test_fetch_apod_success():
    from src.services.nasa_client import fetch_apod
    with patch("src.services.nasa_client._session.get") as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "date": "2025-08-16", "title": "Test",
            "media_type": "image", "url": "https://example.com/img.jpg",
        }
        data = fetch_apod()
        assert data["title"] == "Test"
