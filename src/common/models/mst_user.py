"""ユーザーモデル."""

from copy import deepcopy
from typing import cast

from sqlalchemy import DATE, INTEGER
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from models import Database


def get_data(logger, db: Database, offset: int, limit: int, condition: dict | None = None):
    """指定された条件に一致するユーザーデータをデータベースから取得します.

    Args:
        logger (Logger): ロガー.
        db (Database): データベースモデル.
        offset (int): 取得を開始する位置.
        limit (int): 取得する最大のレコード数.
        condition (dict, optional): フィルタリング条件. Defaults to None.

    Yields:
        mst_user: 指定された条件に一致するユーザーデータ
    """
    with db.session_scope() as session:
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
                    if isinstance(column_type, (INTEGER, DATE)):
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
        yield from query


def get_all_data(logger, db: Database, session: Session | None = None):
    """データベースからすべてのユーザーデータを取得します.

    Args:
        logger (Logger): ロガー.
        db (Database): データベースモデル.
        session (Session | None, optional): 既存のセッション.
            指定された場合はそれを使用します(同じトランザクション内で操作する場合).

    Yields:
        mst_user: データベースから取得したユーザーデータ
    """
    # 既存のセッションが渡された場合はそれを使用
    if session is not None:
        # session は None でないことが保証されているが、型チェッカーが認識しないため cast を使用
        active_session: Session = cast("Session", session)
        # db.mst_user は実行時に設定されるため、型チェッカーには None の可能性があると判断される
        query = active_session.query(db.mst_user)  # type: ignore
        logger.debug(query)
        yield from query
    else:
        # 新しいセッションを作成
        with db.session_scope() as new_session:
            query = new_session.query(db.mst_user)
            logger.debug(query)
            yield from query


def get_user_by_user_id(logger, db: Database, user_id: str):
    """指定されたユーザーIDに一致するユーザーをデータベースから取得します.

    Args:
        logger (Logger): ロガー.
        db (Database): データベースモデル.
        user_id (str): ユーザーID.

    Returns:
        mst_user: ユーザーIDに一致するユーザー. 見つからない場合は None.
    """
    user = None
    with db.session_scope() as session:
        query = session.query(db.mst_user).filter(db.mst_user.user_id == user_id)
        logger.debug(query)
        user = deepcopy(query.first())
    return user
