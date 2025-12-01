"""設定."""

import os


def get_config():
    """環境変数 POSITION に応じて Config を返す."""
    if os.environ.get("POSITION", "") == "PRD":
        return PrdConfig
    elif os.environ.get("POSITION", "") == "STG":
        return StgConfig
    elif os.environ.get("POSITION", "") == "DEV":
        return DevConfig
    return LocalConfig


class Config:
    """設定."""

    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://myaccount:myaccount@192.168.33.33/mydb"


class LocalConfig(Config):
    """ローカル環境の設定."""

    DEBUG = True


class DevConfig(Config):
    """開発環境の設定."""

    DEBUG = True


class StgConfig(Config):
    """ステージング環境の設定."""

    DEBUG = False


class PrdConfig(Config):
    """本番環境の設定."""

    DEBUG = False
