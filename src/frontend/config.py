import datetime
import os
import secrets


def get_config():
    if os.environ.get("POSITION", "") == "PRD":
        # ローカルしかないけどね
        return LocalConfig
    elif os.environ.get("POSITION", "") == "STG":
        # ローカルしかないけどね
        return LocalConfig
    elif os.environ.get("POSITION", "") == "DEV":
        # ローカルしかないけどね
        return LocalConfig
    return LocalConfig


class Config:

    SECRET_KEY = secrets.token_hex()
    SESSION_COOKIE_NAME = "SONY信者"
    SESSION_COOKIE_SAMESITE = "Strict"
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=4)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = secrets.token_hex(16)
    WTF_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]


class LocalConfig(Config):

    DEBUG = True
