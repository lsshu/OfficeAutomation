import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'sqlite:///{}'.format(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "db.sqlite3"))
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@43.129.74.20:3306/oa"  # MySQL或PostgreSQL的连接方法

Engine = create_engine(
    # echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志
    # 由于SQLAlchemy是多线程，指定check_same_thread=False来让建立的对象任意线程都可使用。这个参数只在用SQLite数据库时设置
    SQLALCHEMY_DATABASE_URL, encoding='utf-8',
    # echo=True,
    pool_pre_ping=True,
    pool_size=100, pool_recycle=3600, max_overflow=100,
    connect_args={
        # 'check_same_thread': False,
        "charset": "utf8mb4"
    }
)

# 在SQLAlchemy中，CRUD都是通过会话(session)进行的，所以我们必须要先创建会话，每一个SessionLocal实例就是一个数据库session
# flush()是指发送数据库语句到数据库，但数据库不一定执行写入磁盘；commit()是指提交事务，将变更保存到数据库文件
SessionLocal = sessionmaker(bind=Engine, autoflush=False, autocommit=False, expire_on_commit=True)

# 创建基本映射类
Model = declarative_base(bind=Engine, name='Model')


def to_dict(self):
    """
    ORM转dict
    :param self:
    :return:
    """
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


Model.to_dict = to_dict
