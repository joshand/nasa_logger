from __future__ import annotations
from pathlib import Path
from urllib.parse import urlparse
import requests


def save_image_to_static(url: str, date_str: str, rel_root: str = "epic") -> str:
    """
    Download `url` into src/static/<rel_root>/YYYY/MM/DD/<filename>
    Returns the relative path to use with url_for('static', filename=...).
    """
    if not url:
        return ""

    # Extract YYYY-MM-DD safely (EPIC `date` often includes time)
    y, m, d = date_str[:10].split("-")  # "YYYY", "MM", "DD"

    # Resolve static dir: src/static
    static_dir = Path(__file__).resolve().parents[1] / "static"
    dest_dir = static_dir / rel_root / y / m / d
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Use the filename from the URL path, strip query params
    parsed = urlparse(url)
    filename = Path(parsed.path).name or "image.png"
    dest = dest_dir / filename

    # Skip re-download if it exists
    if not dest.exists():
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        dest.write_bytes(resp.content)

    # Return path relative to static/ so Flask can serve it
    rel_path = f"{rel_root}/{y}/{m}/{d}/{filename}"
    return rel_path
