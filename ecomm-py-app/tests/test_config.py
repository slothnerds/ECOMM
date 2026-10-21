from datetime import timedelta

import pytest
from pydantic import SecretStr, ValidationError

from ecommerce.core.config import Settings, get_settings

VALID_SECRET = "a-valid-secret-that-is-32-chars-long!"


def test_valid_settings_are_parsed() -> None:
    # model_validate parses raw values the way environment variables arrive (as strings)
    settings = Settings.model_validate({"jwt_secret": VALID_SECRET, "hold_duration": "PT15M"})

    assert settings.hold_duration == timedelta(minutes=15)
    assert settings.environment == "test"  # from conftest.py's APP_ENV


def test_secret_is_masked_when_printed() -> None:
    settings = Settings(jwt_secret=SecretStr(VALID_SECRET))

    assert VALID_SECRET not in repr(settings)
    assert str(settings.jwt_secret) == "**********"
    assert settings.jwt_secret.get_secret_value() == VALID_SECRET


def test_short_jwt_secret_is_rejected() -> None:
    with pytest.raises(ValidationError, match="at least 32"):
        Settings(jwt_secret=SecretStr("too-short"))


def test_unknown_environment_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "staging")

    with pytest.raises(ValidationError, match="APP_ENV"):
        Settings(jwt_secret=SecretStr(VALID_SECRET))


@pytest.mark.parametrize(("profile", "port"), [("local", 5433), ("docker", 5432)])
def test_profile_selects_the_database(
    monkeypatch: pytest.MonkeyPatch, profile: str, port: int
) -> None:
    monkeypatch.setenv("APP_PROFILE", profile)
    # conftest points DB_* at the test container; drop them so the profile files apply
    for name in ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"):
        monkeypatch.delenv(name, raising=False)
    get_settings.cache_clear()  # get_settings caches; start fresh for this profile
    try:
        settings = get_settings()

        assert settings.profile == profile
        assert settings.db_port == port
        assert (
            settings.database_url
            == f"postgresql+psycopg://postgres:password@localhost:{port}/ecomm_db"
        )
        assert "password" not in settings.database_display  # safe to log
    finally:
        get_settings.cache_clear()  # don't leak this profile into other tests


def test_default_profile_is_local(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("APP_PROFILE", raising=False)
    monkeypatch.delenv("DB_PORT", raising=False)
    get_settings.cache_clear()
    try:
        assert get_settings().db_port == 5433
    finally:
        get_settings.cache_clear()
