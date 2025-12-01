"""設定."""

import datetime
import os
from typing import ClassVar


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
    """初期設定."""

    # セッションやCSRF保護に使用される秘密鍵
    # python -c 'import secrets; print(secrets.token_hex())'
    SECRET_KEY = "c7c8404a9f646389892066653645993e3cef05171a91ea6d2ed698e9026b2d05"
    # セッションクッキーの名前
    SESSION_COOKIE_NAME = "landwarrior"
    # クッキーのSameSite属性をStrictに設定し、クロスサイトリクエストでの送信を防ぐ
    SESSION_COOKIE_SAMESITE = "Strict"
    # クッキーへのアクセスをHTTP(S)通信のみに限定し、JavaScriptからのアクセスを防ぐ
    SESSION_COOKIE_HTTPONLY = True
    # セッションの有効期限を4時間に設定
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=4)
    # CSRF保護を有効化
    WTF_CSRF_ENABLED = True
    # CSRFトークンのための秘密鍵
    # python -c 'import secrets; print(secrets.token_hex(16))'
    WTF_CSRF_SECRET_KEY = "0aa0ff26473e8ed28898c21cbdebc645"
    # CSRF保護を適用するHTTPメソッド
    #   注意: リストや辞書などの可変オブジェクトをクラス属性として定義する場合、
    #   ClassVar でアノテートする必要があります。これにより型チェッカーは
    #   その属性がインスタンス属性ではなくクラス属性であることを認識し、
    #   可変オブジェクトの共有による予期しない動作を防ぎます。
    WTF_CSRF_METHODS: ClassVar[list[str]] = ["POST", "PUT", "PATCH", "DELETE"]
    # CSRFトークンの有効期限を秒で設定( 14400 秒 = 4 時間)
    WTF_CSRF_TIME_LIMIT = 14400
    # バックエンドサービスのURL
    BACKEND_URL = "http://backend:5000"


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
