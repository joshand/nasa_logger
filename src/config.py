import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    nasa_api_key: str
    database_url: str
    flask_env: str

    def __init__(self) -> None:
        self.nasa_api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./apod.db")
        self.flask_env = os.getenv("FLASK_ENV", "production")


settings = Settings()
