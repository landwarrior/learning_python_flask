from copy import deepcopy

from models import Database, session_scope
from sqlalchemy import DATE, INTEGER, Engine
from sqlalchemy.sql import func


def get_data(logger, engine: Engine, db: Database, offset: int, limit: int, condition: dict = None):
    """
    指定された条件に一致するユーザーデータをデータベースから取得します.

    Args:
        logger (Logger): ロガー.
        engine (Engine): SQLAlchemyのエンジン.
        db (Database): データベースモデル.
        offset (int): 取得を開始する位置.
        limit (int): 取得する最大のレコード数.
        condition (dict, optional): フィルタリング条件. Defaults to None.

    Yields:
        mst_user: 指定された条件に一致するユーザーデータ
    """
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
                        query = query.filter(getattr(db.mst_user, key).like(f"%{value}%"))
                elif key.endswith("_from") and hasattr(db.mst_user, key[:-5]):
                    query = query.filter(getattr(db.mst_user, key[:-5]) >= value)
                elif key.endswith("_to") and hasattr(db.mst_user, key[:-3]):
                    query = query.filter(getattr(db.mst_user, key[:-3]) <= value)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        logger.debug(query)
        for user in query:
            yield user


def get_all_data(logger, engine: Engine, db: Database):
    """データベースからすべてのユーザーデータを取得します.

    Args:
        logger (Logger): ロガー.
        engine (Engine): SQLAlchemyのエンジン.
        db (Database): データベースモデル.

    Yields:
        mst_user: データベースから取得したユーザーデータ
    """
    with session_scope(engine) as session:
        query = session.query(db.mst_user)
        logger.debug(query)
        for user in query:
            yield user


def get_user_by_user_id(logger, engine: Engine, db: Database, user_id: str):
    """指定されたユーザー名に一致するユーザーをデータベースから取得します.

    Args:
        logger (Logger): ロガー.
        engine (Engine): SQLAlchemyのエンジン
        db (Database): データベースモデル
        user_id (str): ユーザーID

    Returns:
        mst_user: ユーザーIDに一致するユーザー
    """
    user = None
    with session_scope(engine) as session:
        query = session.query(db.mst_user).filter(db.mst_user.user_id == user_id)
        logger.debug(query)
        user = deepcopy(query.first())
    return user
