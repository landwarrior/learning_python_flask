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

    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://myaccount:myaccount@192.168.33.33/mydb"


class LocalConfig(Config):

    DEBUG = True
