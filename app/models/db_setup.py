from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import config

engine = create_engine(f'postgresql://postgres:'
                       f'{config.password}@localhost:{config.port}/{config.db_name}')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()


# create the db
def init_db():
    from models.entities import Role
    from models.entities import UserAccount
    Base.metadata.create_all(engine)
