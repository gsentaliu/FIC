from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:postgres@db:5432/postgres')
Session = Session(bind=engine)

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

class Word(Base):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    word = Column(String)