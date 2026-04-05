"""SQLAlchemy Declarative Base."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """宣言的ベースクラス.

    各 ORM テーブルクラスの共通基底です。SQLAlchemy 2.0 では ``declarative_base()`` の
    ファクトリではなく、``DeclarativeBase`` を継承して Base を定義する方式が推奨されます。
    """
