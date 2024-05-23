import bcrypt
from models import Database, mst_user


def main():
    new_password = b"password"

    db = Database("mysql+mysqlconnector://myaccount:myaccount@192.168.33.33/mydb")
    db.Base.prepare(autoload_with=db.engine)
    db.mst_user = db.Base.classes.mst_user

    for user in mst_user.get_all_data(db.engine, db):
        user.ignition_key = bcrypt.hashpw(new_password, bcrypt.gensalt())


if __name__ == "__main__":
    main()
