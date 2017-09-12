import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

conn = sa.create_engine('mysql+pymysql://admin:Adm!n2017@192.168.33.10/test?charset=utf8')

Base = declarative_base()

class User(Base):
    """usersテーブルを定義."""
    __tablename__ = 'users'
    user_id = sa.Column('user_id', sa.Integer, primary_key=True, autoincrement=False)
    user_name = sa.Column('user_name', sa.String(200), nullable=False, unique=True)
    password = sa.Column('password', sa.String(200), nullable=False)
    active = sa.Column('active', sa.Integer, nullable=False)
    create_date = sa.Column('create_date', sa.DateTime)
    update_date = sa.Column('update_date', sa.DateTime)
    delete_date = sa.Column('delete_date', sa.DateTime)

    def __init__(self, user_id, user_name, password, active, create_date, update_date, delete_date):
        """コンストラクタ."""
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

    @classmethod
    def get_data(cls, user_name=None):
        if user_name is None:
            listdata = list()
            Session = sessionmaker(bind=conn)
            session = Session()
            for data in session.query(cls):
                listdata.append({
                    'user_id': data.user_id,
                    'user_name': data.user_name,
                    'password': data.password,
                    'active': data.active,
                    'create_date': data.create_date,
                    'update_date': data.update_date,
                    'delete_date': data.delete_date
                    })
            session.close()
            return listdata
        else:
            try:
                Session = sessionmaker(bind=conn)
                session = Session()
                data = session.query(cls).filter(cls.user_name == user_name).one()
                return data
            except Exception as e:
                return None

    @classmethod
    def insert_new_data(cls, listdata):
        """データのインサート.
        
        形式は以下を想定
        [
            {
                "user_id": something,
                "user_name": something,
                "password": something,
                "active": [1|0],
                "create_date": None (or YYYMMDDhhmmss and so on),
                "update_date": None (or YYYMMDDhhmmss and so on),
                "delete_date": None (or YYYMMDDhhmmss and so on)
            }
        ]
        """
        Session = sessionmaker(bind=conn)
        session = Session()
        objects = list()
        for data in listdata:
            object.append(cls(
                data['user_id'],
                data['user_name'],
                data['password'],
                data['active'],
                data['create_date'],
                data['update_date'],
                data['delete_date']
            ))
        # バルクインサート的なやつ
        session.bulk_save_objects(objects)
        # コミット
        session.commit()
        # 接続をクローズ
        session.close()


# これでテーブルがなければ作成される
Base.metadata.create_all(conn)
