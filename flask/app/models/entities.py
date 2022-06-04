from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.db_setup import Base


class Role(Base):
    __tablename__ = 'role_app'
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(40), nullable=False, unique=True)
    users = relationship('UserType', backref='role_app', lazy="joined",
                         cascade='all, delete')

    def dictionarize(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name
        }


class UserType(Base):
    __tablename__ = 'usertype'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_type = Column(String(40), nullable=False)

    fk_role_id = Column(Integer, ForeignKey('role_app.role_id'), nullable=False)

    def dictionarize(self):
        return {
            "user_id": self.user_id,
            "role_name": self.user_type,
            "fk_role_id": self.fk_role_id
        }
