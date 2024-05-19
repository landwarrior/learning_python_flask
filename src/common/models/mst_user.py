from flask import current_app
from models import Database, session_scope
from sqlalchemy import DATE, INTEGER
from sqlalchemy.sql import func


def get_data(engine, db: Database, offset: int, limit: int, condition: dict = None):
    with session_scope(engine) as session:
        query = session.query(
            db.mst_user.user_id.label("user_id"),
            db.mst_user.user_name.label("user_name"),
            db.mst_user.user_name_kana.label("user_name_kana"),
            db.mst_user.email.label("email"),
            db.mst_user.gender.label("gender"),
            db.mst_user.age.label("age"),
            db.mst_user.birth_day.label("birth_day"),
            db.mst_user.blood_type.label("blood_type"),
            db.mst_user.prefecture.label("prefecture"),
            db.mst_user.curry.label("curry"),
            func.count(db.mst_user.user_id).over().label("total"),
        )
        if condition:
            for key, value in condition.items():
                if hasattr(db.mst_user, key):
                    column_type = getattr(db.mst_user, key).type
                    if isinstance(column_type, INTEGER) or isinstance(column_type, DATE):
                        query = query.filter(getattr(db.mst_user, key) == value)
                    else:
                        current_app.logger.info(f"Column {key} type: {column_type}")
                        query = query.filter(getattr(db.mst_user, key).like(f"%{value}%"))
                elif key.endswith("_from") and hasattr(db.mst_user, key[:-5]):
                    query = query.filter(getattr(db.mst_user, key[:-5]) >= value)
                elif key.endswith("_to") and hasattr(db.mst_user, key[:-3]):
                    query = query.filter(getattr(db.mst_user, key[:-3]) <= value)
        query = query.offset(offset).limit(limit)
        for cols in query:
            yield cols


def get_user_by_username(engine, db: Database, username: str):
    with session_scope(engine) as session:
        user = session.query(db.mst_user).filter(db.mst_user.user_name == username).first()
        return user
