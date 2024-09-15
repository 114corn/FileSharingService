from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, backref
import os
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    files = relationship('File', backref='owner')

    def __repr__(self):
        return f'<User {self.username}>'

    @staticmethod
    def add_user(username, email):
        try:
            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()
            return f'User {username} added successfully!'
        except SQLAlchemyError as e:
            db.session.rollback()
            return f'Error: {str(e)}'

class File(db.Model):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    path = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<File {self.name}>'

    @staticmethod
    def add_file(name, path, user_id):
        try:
            new_file = File(name=name, path=path, user_id=user_id)
            db.session.add(new_file)
            db.session.commit()
            return f'File {name} added successfully!'
        except SQLAlchemyError as e:
            db.session.rollback()
            return f'Error: {str(e)}'

@app.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(error):
    return jsonify({'error': str(error)}), 500

@app.route('/')
def index():
    return "Welcome to the FileSharingService"

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)