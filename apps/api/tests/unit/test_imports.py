from bookverse.config import Settings
from bookverse.models import Base, BookCategory, CanonicalAuthor, CanonicalBook


def test_settings_defaults():
    s = Settings()
    assert s.app_env == "local"
    assert s.api_prefix == "/api"
    assert s.db_host == "127.0.0.1"


def test_models_importable():
    assert issubclass(CanonicalBook, Base)
    assert issubclass(CanonicalAuthor, Base)
    assert issubclass(BookCategory, Base)
