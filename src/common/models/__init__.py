from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool


@contextmanager
def session_scope(engine):
    """データベースセッションのスコープを提供するコンテキストマネージャ.

    このコンテキストマネージャを使用することで、セッションの開始から終了までの処理を自動で行うことができます。
    例外が発生した場合はロールバックされ、処理が終了するとセッションは閉じられ、エンジンも破棄されます。

    使用例:
        with session_scope(engine) as session:
            session.add(some_object)
            session.query(SomeModel).filter_by(some_criteria).all()

    このコンテキスト内で行われた変更は、例外が発生しなければコミットされます。
    """
    session = Session(bind=engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        engine.dispose()


class Database:
    """Flask の app に登録するためのクラス."""

    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string, poolclass=NullPool)
        self.Base = automap_base()
        self.mst_user = None
