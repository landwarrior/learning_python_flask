"""データベースモデル."""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

from .base import Base
from .mst_user_model import MstUser


class Database:
    """Flask の app に登録するためのクラス."""

    def __init__(self, connection_string: str):
        """コンストラクタ.

        Args:
            connection_string (str): データベース接続文字列.
        """
        self.engine = create_engine(connection_string, poolclass=NullPool)

    @contextmanager
    def session_scope(self, session: Session | None = None):
        """データベースセッションのスコープを提供するコンテキストマネージャ.

        このメソッドは、この Database インスタンスのエンジンを使用して
        セッションスコープを提供します。ネストされた呼び出しもサポートしています。

        使用例:
            from models import Database, MstUser

            db = Database(connection_string)
            with db.session_scope() as session:
                # データ取得と更新を同じトランザクション内で実行
                users = session.query(MstUser).all()
                for user in users:
                    user.ignition_key = new_password_hash
                # ブロック正常終了時にコミットされる

            # ネストされた使用(既存のセッションを再利用)
            with db.session_scope() as outer_session:
                with db.session_scope(session=outer_session) as inner_session:
                    inner_session.add(another_object)
                # inner はコミットしない。outer 終了時にコミットされる

        新規セッションを開いた場合、例外がなければ ``commit`` し、finally で
        セッションを閉じた後 ``engine.dispose()`` してプールを破棄します。
        ``session`` 引数で既存セッションを渡した場合は yield するだけで、コミット・クローズは
        外側の ``session_scope`` に任せます。

        Args:
            session (Session | None, optional): 既存のセッション.
                指定された場合はそれを使用します(ネストされた呼び出し用).
                この場合、セッションの管理は呼び出し側に委ねられます。

        Yields:
            Session: SQLAlchemyのセッションオブジェクト.
        """
        # 既存のセッションが渡された場合はそれを使用(ネストされた呼び出し)
        if session is not None:
            yield session
            return

        # 新しいセッションを作成
        new_session = Session(bind=self.engine)
        try:
            yield new_session
            new_session.commit()
        except Exception as e:
            new_session.rollback()
            raise e
        finally:
            new_session.close()
            self.engine.dispose()


__all__ = ["Base", "Database", "MstUser"]
