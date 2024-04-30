from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine("mysql+mysqlconnector://myaccount:myaccount@192.168.33.33/mydb")

# reflect the tables
Base.prepare(autoload_with=engine)

# mapped classes are now created with names by default
# matching that of the table name.
mst_user = Base.classes.mst_user


@contextmanager
def session_scope():
    """データベースセッションのスコープを提供するコンテキストマネージャ.

    このコンテキストマネージャを使用することで、セッションの開始から終了までの処理を自動で行うことができます。
    例外が発生した場合はロールバックされ、処理が終了するとセッションは閉じられ、エンジンも破棄されます。

    使用例:
        with session_scope() as session:
            session.add(some_object)
            session.query(SomeModel).filter_by(some_criteria).all()

    このコンテキスト内で行われた変更は、例外が発生しなければコミットされます。
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        engine.dispose()
