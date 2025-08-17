import time
from typing import Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from ..config import settings
from ..logging_setup import logger


BASE_URL = "https://api.nasa.gov/planetary/apod"
BASE_URL_EPIC = "https://api.nasa.gov/EPIC/api/natural"
# BASE_URL_EPIC_DATE = "https://epic.gsfc.nasa.gov/api/enhanced"
_session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=0.3,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=frozenset(["GET"]),            # explicit on urllib3 v2
)
_session.mount("https://", HTTPAdapter(max_retries=retries))


def fetch_apod(date: str | None = None) -> dict[str, Any]:
    params = {"api_key": settings.nasa_api_key}
    if date:
        params["date"] = date
    start = time.perf_counter()
    resp = _session.get(BASE_URL, params=params, timeout=15)
    duration_ms = int((time.perf_counter() - start) * 1000)
    log = logger.bind(event="api_request", endpoint=BASE_URL, status_code=resp.status_code,
                      duration_ms=duration_ms, params={"date": bool(date)})
    if resp.ok:
        log.info("api_request_success")
        return resp.json()
    try:
        details = resp.json()
    except Exception:
        details = {"body": resp.text[:500]}
    log.error("api_request_error", details=details)
    resp.raise_for_status()
    return {}


def fetch_epic(date: str | None = None) -> dict[str, Any]:
    params = {"api_key": settings.nasa_api_key}
    if date:
        new_url = BASE_URL_EPIC + f"/date/{date}"
    else:
        new_url = BASE_URL_EPIC + f"/images"

    start = time.perf_counter()
    resp = _session.get(new_url, params=params, timeout=15)
    duration_ms = int((time.perf_counter() - start) * 1000)
    log = logger.bind(event="api_request", endpoint=new_url, status_code=resp.status_code,
                      duration_ms=duration_ms, params={"date": bool(date)})
    if resp.ok:
        log.info("api_request_success")
        resp_json = resp.json()
        # print(resp_json)
        if type(resp_json) == list:
            if len(resp_json) > 0:
                return resp_json[0]
            else:
                return {}
        elif type(resp_json) == dict:
            return resp_json
        else:
            return {}
    try:
        details = resp.json()
    except Exception:
        details = {"body": resp.text[:500]}
    log.error("api_request_error", details=details)
    resp.raise_for_status()
    return {}
