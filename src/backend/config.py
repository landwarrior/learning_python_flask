"""設定."""


def get_config():
    """環境変数 POSITION に応じて Config を返す."""
    # 現在はローカルの設定しかないのでコメントアウト
    # if os.environ.get("POSITION", "") == "PRD":
    #     return LocalConfig
    # elif os.environ.get("POSITION", "") == "STG":
    #     return LocalConfig
    # elif os.environ.get("POSITION", "") == "DEV":
    #     return LocalConfig
    return LocalConfig


class Config:
    """設定."""

    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://myaccount:myaccount@192.168.33.33/mydb"


class LocalConfig(Config):
    """ローカル環境の設定."""

    DEBUG = True
