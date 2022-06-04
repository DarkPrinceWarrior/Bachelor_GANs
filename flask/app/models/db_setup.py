from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('postgresql://postgres:123@localhost:5432/gen_Imagedb')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()


# create the db
def init_db():
    from models.entities import Role
    from models.entities import UserType
    Base.metadata.create_all(engine)
