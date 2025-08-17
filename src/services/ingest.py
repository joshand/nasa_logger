from typing import Any
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from src.db import SessionLocal
from src.models import Image
from src.logging_setup import logger
from src.services.nasa_client import fetch_apod, fetch_epic
from ..config import settings
from .files import save_image_to_static


def normalize_apod(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "date": record.get("date"),
        "title": record.get("title") or "Untitled",
        "media_type": record.get("media_type") or "unknown",
        "url": record.get("url") or "",
        "hdurl": record.get("hdurl"),
        "explanation": record.get("explanation"),
        "local_path": None,
    }


def normalize_epic(record: dict[str, Any]) -> dict[str, Any]:
    date_id = record.get("identifier")
    image_name = record.get("image")
    if not date_id or not image_name:
        url = ""
    else:
        year = str(date_id[0:4])
        month = str(date_id[4:6])
        day = str(date_id[6:8])
        url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={settings.nasa_api_key}"

    return {
        "date": record.get("date"),
        "title": record.get("caption") or "Untitled",
        "media_type": "unknown",
        "url": url,
        "hdurl": "",
        "explanation": "",
        "local_path": None,
    }


def ingest_apod(date: str | None = None) -> Image:
    raw = fetch_apod(date)
    data = normalize_apod(raw)

    with SessionLocal() as session:
        existing = session.execute(select(Image).where(Image.date == data["date"])).scalar_one_or_none()
        if existing:
            for k, v in data.items():
                setattr(existing, k, v)
            session.commit()
            logger.info("apod_update", date=data["date"], mode="update")
            return existing
        apod = Image(**data)
        session.add(apod)
        try:
            session.commit()
            logger.info("apod_insert", date=data["date"], mode="insert")
            return apod
        except IntegrityError as e:
            session.rollback()
            logger.error("db_integrity_error", error=str(e), date=data["date"])
            raise


def ingest_epic(date: str | None = None) -> Image:
    raw = fetch_epic(date)
    if raw == {}:
        logger.error("image_fetch_error", error="Unable to fetch image", date=str(date))
        raise ValueError("Unable to fetch image")

    data = normalize_epic(raw)

    try:
        data["local_path"] = save_image_to_static(data["url"], data["date"], rel_root="epic") if data["url"] else ""
        if data["local_path"]:
            logger.info("image_saved", local_path=data["local_path"], date=data["date"])
    except Exception as e:
        logger.error("image_download_error", error=str(e), url=data["url"], date=data["date"])
        data["local_path"] = ""

    with SessionLocal() as session:
        existing = session.execute(select(Image).where(Image.date == data["date"])).scalar_one_or_none()
        if existing:
            for k, v in data.items():
                setattr(existing, k, v)
            session.commit()
            logger.info("epic_update", date=data["date"], mode="update")
            return existing
        epic = Image(**data)
        session.add(epic)
        try:
            session.commit()
            logger.info("epic_insert", date=data["date"], mode="insert")
            return epic
        except IntegrityError as e:
            session.rollback()
            logger.error("db_integrity_error", error=str(e), date=data["date"])
            raise


def download_image(url: str) -> str:
    local_path = "/images/" + url.split("/")[-1]