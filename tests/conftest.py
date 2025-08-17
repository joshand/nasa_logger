import pytest


@pytest.fixture(autouse=True)
def _test_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("NASA_API_KEY", "DEMO_KEY")
    from src.app import create_app
    from src.db import Base, engine
    app = create_app()
    with app.app_context():
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    yield
