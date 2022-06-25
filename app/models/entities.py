from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.db_setup import Base


class Role(Base):
    __tablename__ = 'role'
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(40), nullable=False, unique=True)

    usertypes = relationship('Usertype', backref='role', lazy="joined",
                             cascade='all, delete')

    def dictionarize(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name
        }


class Usertype(Base):
    __tablename__ = 'usertype'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_token = Column(String(255), nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey('role.role_id'), nullable=False)

    users = relationship('UserAccount', backref='usertype', lazy="joined",
                         cascade='all, delete')

    companies = relationship('CompanyAccount', backref='usertype', lazy="joined",
                             cascade='all, delete')

    images = relationship('Image', backref='usertype', lazy="joined",
                          cascade='all, delete')

    def dictionarize(self):
        return {
            "user_id": self.user_id,
            "user_token": self.user_token,
            "role_id": self.role_id
        }


class UserAccount(Base, UserMixin):
    __tablename__ = 'user_account'

    phy_id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(40), nullable=False, unique=True)
    email = Column(String(40), nullable=False, unique=True)
    phyone_password = Column(String(255), nullable=False)
    subscription_ = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey('usertype.user_id'), nullable=False, unique=True)

    def get_id(self):
        return self.phy_id

    def dictionarize(self):
        return {
            "phy_id": self.phy_id,
            "login": self.login,
            "email": self.email,
            "phyone_password": self.phyone_password,
            "subscription": self.subscription,
            "user_id": self.user_id
        }


class CompanyAccount(Base):
    __tablename__ = 'company_account'

    jur_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(40), nullable=False, unique=True)
    legal_address = Column(String(40), nullable=False, unique=True)
    post_address = Column(String(40), nullable=False, unique=True)
    tin = Column(String(40), nullable=False, unique=True)
    director = Column(String(40), nullable=False, unique=True)
    email = Column(String(40), nullable=False, unique=True)
    phone_number = Column(String(40), nullable=False)
    website = Column(String(40), nullable=False)
    jurone_password = Column(String(255), nullable=False)
    subscription_ = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey('usertype.user_id'), nullable=False, unique=True)

    def dictionarize(self):
        return {
            "jur_id": self.jur_id,
            "company_name": self.company_name,
            "legal_address": self.legal_address,
            "post_address": self.post_address,
            "tin": self.tin,
            "director": self.director,
            "email": self.email,
            "phone_number": self.phone_number,
            "website": self.website,
            "jurone_password": self.jurone_password,
            "subscription": self.subscription,
            "user_id": self.user_id
        }


class Image(Base):
    __tablename__ = 'image'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    image_path = Column(String(100), nullable=False)
    fk_user_id = Column(Integer, ForeignKey('usertype.user_id'), nullable=False)

    def dictionarize(self):
        return {
            "image_id": self.image_id,
            "image_path": self.image_path,
            "fk_user_id": self.fk_user_id
        }
