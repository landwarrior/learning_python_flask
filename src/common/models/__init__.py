"""データベースモデル."""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool


class Database:
    """Flask の app に登録するためのクラス."""

    def __init__(self, connection_string: str):
        """コンストラクタ.

        Args:
            connection_string (str): データベース接続文字列.
        """
        self.engine = create_engine(connection_string, poolclass=NullPool)
        self.Base = automap_base()
        self.mst_user = None

    @contextmanager
    def session_scope(self, session: Session | None = None):
        """データベースセッションのスコープを提供するコンテキストマネージャ.

        このメソッドは、この Database インスタンスのエンジンを使用して
        セッションスコープを提供します。ネストされた呼び出しもサポートしています。

        使用例:
            db = Database(connection_string)
            db.Base.prepare(autoload_with=db.engine)
            db.mst_user = db.Base.classes.mst_user
            with db.session_scope() as session:
                # データ取得と更新を同じトランザクション内で実行
                users = session.query(db.mst_user).all()
                for user in users:
                    user.ignition_key = new_password_hash
                # 自動的にコミットされる

            # ネストされた使用(既存のセッションを再利用)
            with db.session_scope() as outer_session:
                # 既存のセッションを渡すことで、同じトランザクション内で操作
                with db.session_scope(session=outer_session) as inner_session:
                    inner_session.add(another_object)

        このコンテキスト内で行われた変更は、例外が発生しなければコミットされます。
        ネストされた場合、最も外側のコンテキストでコミットされます。
        コンテキストを抜ける際に、セッションは自動的に閉じられ、エンジンの接続もクリーンアップされます。

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
