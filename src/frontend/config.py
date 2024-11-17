import datetime
import os


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
    WTF_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
    # CSRFトークンの有効期限を秒で設定（14400秒 = 4時間）
    WTF_CSRF_TIME_LIMIT = 14400
    # バックエンドサービスのURL
    BACKEND_URL = "http://backend:5000"


class LocalConfig(Config):

    DEBUG = True
