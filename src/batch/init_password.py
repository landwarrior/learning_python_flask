import logging
import os

import bcrypt

from models import Database, mst_user
from mylogger import UniqueKeyFormatter


def main():
    new_password = b"password"
    logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = UniqueKeyFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    db = Database("mysql+mysqlconnector://myaccount:myaccount@192.168.33.33/mydb")
    db.Base.prepare(autoload_with=db.engine)
    db.mst_user = db.Base.classes.mst_user

    for user in mst_user.get_all_data(logger, db.engine, db):
        logger.info(f"ユーザーID: {user.user_id}")
        user.ignition_key = bcrypt.hashpw(new_password, bcrypt.gensalt())


if __name__ == "__main__":
    main()
