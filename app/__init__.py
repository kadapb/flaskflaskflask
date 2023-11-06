from flask import Flask
from app.database import User
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
import os

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'your_secret_key_here'

login_manager = LoginManager()
login_manager.login_view = "sign_in"
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sportDB.db'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

Base = declarative_base()
Base.metadata.create_all(db)

Session = sessionmaker(bind=db)
session = Session()

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))


from app import admin_views, views