from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin

engine = create_engine('sqlite:///sportDB.db')
Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column('username', String(50), nullable=False, unique=True)
    password = Column('password', String(50), nullable=False)


class MenuItem(Base):
    __tablename__ = 'MenuItems'
    id = Column(Integer, primary_key=True)
    name = Column('MenuItemName', String)
    url = Column('url', String)
    
    def __init__(self, name, url):
        self.name = name
        self.url = url
    
    def __repr__(self):
        return f"{self.name}, {self.url}"
    
class MenuItemUser(Base):
    __tablename__ = 'MenuItemsUser'
    id = Column(Integer, primary_key=True)
    name = Column('MenuItemName', String)
    url = Column('url', String)
    
    def __init__(self, name, url):
        self.name = name
        self.url = url
    
    def __repr__(self):
        return f"{self.name}, {self.url}"    
    


class Cheese(Base):
    __tablename__ = 'cheeses'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), nullable=False)
    description = Column('description', String)
    cheese_type = Column('cheese_type', String(50))
    origin = Column('origin', String(50))
    milk = Column('milk', String(50))
    img_name = Column('img_name', String(100), nullable=False)
    




Base.metadata.create_all(engine)