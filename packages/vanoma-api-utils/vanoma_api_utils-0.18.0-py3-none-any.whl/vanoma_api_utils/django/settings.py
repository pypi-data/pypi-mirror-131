import os
import dj_database_url  # type: ignore
from typing import Any, Dict


def resolve_environment() -> str:
    return os.environ.get("ENVIRONMENT", "testing")


def resolve_debug() -> bool:
    return resolve_environment() != "production"


def resolve_database() -> Dict[str, str]:
    if resolve_environment() == "testing":
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join("/tmp", "db.sqlite3"),
        }

    return dj_database_url.config(conn_max_age=600)


def resolve_logging() -> Dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"] if resolve_environment() != "testing" else [],
            "level": "INFO",
        },
    }
