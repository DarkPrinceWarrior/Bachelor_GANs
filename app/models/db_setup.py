from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import config
from deta import Deta  # Import Deta
from config import deta_project_key  # project key for deta

engine = create_engine(f'postgresql://postgres:'
                       f'{config.password}@localhost:{config.port}/{config.db_name}')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()


# Initialize with a Project Key
deta = Deta(deta_project_key)
# This how to connect to or create a database.
drive = deta.Drive("photo_drive")
# You can create as many as you want
photos = deta.Drive("photos")


# create the db
def init_db():
    from models.entities import Role
    from models.entities import UserAccount
    Base.metadata.create_all(engine)
