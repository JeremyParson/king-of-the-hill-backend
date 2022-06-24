import enum
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, TEXT
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

db = SQLAlchemy()
Base = declarative_base()


class Character (db.Model):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    hill_id = Column(Integer, ForeignKey("hills.id"))
    name = Column(String(250))
    image = Column(String(250))
    description = Column(TEXT)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Hill (db.Model):
    __tablename__ = 'hills'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(250))
    image = Column(String(250))
    description = Column(TEXT)
    hills = relationship("Character")

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Roles (enum.Enum):
    user = 1
    admin = 2


class Users (db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    username = Column(String(250))
    password_digest = Column(String(250))
    role = Column(Enum(Roles))
    hills = relationship("Hill")

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
