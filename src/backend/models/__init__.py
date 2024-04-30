from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = automap_base()


def initialize_engine(connection_string):
    """データベースエンジンを初期化する関数です。

    Args:
        connection_string (str): データベースへの接続文字列。

    Returns:
        Engine: SQLAlchemy Engine インスタンス。
    """
    return create_engine(connection_string)


# engine の初期化は外部から行う
# 例: engine = initialize_engine("mysql+mysqlconnector://myaccount:myaccount@host/mydb")

# reflect the tables
# Base.prepare(autoload_with=engine) は engine が初期化された後に呼び出す必要がある

# mapped classes are now created with names by default
# matching that of the table name.
# mst_user = Base.classes.mst_user は Base が準備された後にアクセスする


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

    def __init__(self):
        self.engine = None
        self.Base = None
        self.mst_user = None
