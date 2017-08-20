import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

conn = sa.create_engine('mysql+pymysql://admin:Adm!n2017@192.168.0.202/test?charset=utf8')

Base = declarative_base()

class User(Base):
    """usersテーブルを定義"""
    __tablename__ = 'users'
    user_id = sa.Column('user_id', sa.Integer, primary_key=True, autoincrement=False)
    user_name = sa.Column('user_name', sa.String(200), nullable=False)
    password = sa.Column('password', sa.String(200), nullable=False)
    active = sa.Column('active', sa.Integer, nullable=False)
    create_date = sa.Column('create_date', sa.DateTime)
    update_date = sa.Column('update_date', sa.DateTime)
    delete_date = sa.Column('delete_date', sa.DateTime)
    def __init__(self, user_id, user_name, password, active, create_date, update_date, delete_date):
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.active = active
        self.create_date = create_date
        self.update_date = update_date
        self.delete_date = delete_date
    def __repr__(self):
        return "<User({}, {}, {}, {}, {}, {}, {})>".format(
            self.user_id, self.user_name, self.password, self.active,
            self.create_date, self.update_date, self.delete_date)

# これでテーブルがなければ作成される
Base.metadata.create_all(conn)

# データを追加するには以下のようにすればいいはずだと思うけどなぜかデータが入らない
insert = User(None, 'test_user', 'password', 1, None, None, None)