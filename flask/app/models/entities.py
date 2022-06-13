from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.db_setup import Base


class Role(Base):
    __tablename__ = 'role_app'
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(40), nullable=False, unique=True)

    physicalusers = relationship('PhysUser', backref='role_app', lazy="joined",
                         cascade='all, delete')
    juridicalusers = relationship('JuridUser', backref='role_app', lazy="joined",
                         cascade='all, delete')

    def dictionarize(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name
        }


class PhysUser(Base):
    __tablename__ = 'phyone'

    phy_id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(40), nullable=False, unique=True)
    email = Column(String(40), nullable=False, unique=True)
    phyone_password = Column(String(40), nullable=False)
    subscription_ = Column(Boolean, nullable=False)

    role_id = Column(Integer, ForeignKey('role_app.role_id'), nullable=False)

    images = relationship('Image', backref='phyone', lazy="joined",
                          cascade='all, delete')

    def dictionarize(self):
        return {
            "phy_id": self.phy_id,
            "login": self.login,
            "email": self.email,
            "phyone_password": self.phyone_password,
            "subscription": self.subscription,
            "role_id": self.fk_role_id
        }


class JuridUser(Base):
    __tablename__ = 'jurone'

    jur_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(40), nullable=False, unique=True)
    legal_address = Column(String(40), nullable=False, unique=True)
    post_address = Column(String(40), nullable=False, unique=True)
    tin = Column(String(40), nullable=False, unique=True)
    director = Column(String(40), nullable=False, unique=True)
    email = Column(String(40), nullable=False, unique=True)
    phone_number = Column(String(40), nullable=False)
    website = Column(String(40), nullable=False)
    jurone_password = Column(String(40), nullable=False)
    subscription_ = Column(Boolean, nullable=False)

    role_id = Column(Integer, ForeignKey('role_app.role_id'), nullable=False)

    images = relationship('Image', backref='jurone', lazy="joined",
                          cascade='all, delete')

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
            "role_id": self.fk_role_id
        }


class Image(Base):
    __tablename__ = 'image'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    image_path = Column(String(40), nullable=False, unique=True)

    fk_jur_id = Column(Integer, ForeignKey('jurone.jur_id'), nullable=False)
    fk_phy_id = Column(Integer, ForeignKey('phyone.phy_id'), nullable=False)

    def dictionarize(self):
        return {
            "image_id": self.image_id,
            "image_path": self.image_path,
            "fk_jur_id": self.fk_jur_id,
            "fk_phy_id": self.fk_phy_id
        }
