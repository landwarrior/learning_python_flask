"""ユーザーモデル."""

from copy import deepcopy
from typing import TYPE_CHECKING

from sqlalchemy import DATE, INTEGER
from sqlalchemy.sql import func

from models import Database, MstUser


if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_data(logger, db: Database, offset: int, limit: int, condition: dict | None = None):
    """指定された条件に一致するユーザーデータをデータベースから取得します.

    Args:
        logger (Logger): ロガー.
        db (Database): エンジンとセッションを管理する Database インスタンス.
        offset (int): 取得を開始する位置.
        limit (int): 取得する最大のレコード数.
        condition (dict, optional): フィルタリング条件. Defaults to None.

    Yields:
        sqlalchemy.engine.Row: 列投影したクエリの行(集計用 ``total`` 列を含む).
    """
    with db.session_scope() as session:
        query = session.query(
            MstUser.user_id.label("user_id"),
            MstUser.user_name.label("user_name"),
            MstUser.user_name_kana.label("user_name_kana"),
            MstUser.email.label("email"),
            MstUser.gender.label("gender"),
            MstUser.age.label("age"),
            MstUser.birth_day.label("birth_day"),
            MstUser.blood_type.label("blood_type"),
            MstUser.prefecture.label("prefecture"),
            MstUser.curry.label("curry"),
            func.count(MstUser.user_id).over().label("total"),
        )
        if condition:
            for key, value in condition.items():
                if hasattr(MstUser, key):
                    column_type = getattr(MstUser, key).type
                    if isinstance(column_type, (INTEGER, DATE)):
                        query = query.filter(getattr(MstUser, key) == value)
                    else:
                        query = query.filter(getattr(MstUser, key).like(f"%{value}%"))
                elif key.endswith("_from") and hasattr(MstUser, key[:-5]):
                    query = query.filter(getattr(MstUser, key[:-5]) >= value)
                elif key.endswith("_to") and hasattr(MstUser, key[:-3]):
                    query = query.filter(getattr(MstUser, key[:-3]) <= value)
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
        db (Database): エンジンとセッションを管理する Database インスタンス.
        session (Session | None, optional): 既存のセッション.
            指定された場合はそれを使用します(同じトランザクション内で操作する場合).

    Yields:
        MstUser: ORM マッピングされたユーザーレコード.
    """
    # 既存のセッションが渡された場合はそれを使用
    if session is not None:
        query = session.query(MstUser)
        logger.debug(query)
        yield from query
    else:
        # 新しいセッションを作成
        with db.session_scope() as new_session:
            query = new_session.query(MstUser)
            logger.debug(query)
            yield from query


def get_user_by_user_id(logger, db: Database, user_id: str):
    """指定されたユーザーIDに一致するユーザーをデータベースから取得します.

    Args:
        logger (Logger): ロガー.
        db (Database): エンジンとセッションを管理する Database インスタンス.
        user_id (str): ユーザーID.

    Returns:
        MstUser | None: 一致する ``MstUser`` のコピー. 見つからない場合は None.
    """
    user = None
    with db.session_scope() as session:
        query = session.query(MstUser).filter(MstUser.user_id == user_id)
        logger.debug(query)
        user = deepcopy(query.first())
    return user
