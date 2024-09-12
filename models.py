from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    files = relationship('File', backref='owner')

    def __repr__(self):
        return f'<User {self.username}>'

class File(db.Model):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    path = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<File {self.name}>'