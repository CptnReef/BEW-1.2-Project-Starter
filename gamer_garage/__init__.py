from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gamer_garage.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from gamer_garage.routes import main
from gamer_garage.routes import auth

app.register_blueprint(main)
app.register_blueprint(auth)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

from gamer_garage.models import User

@login_manager.user_loader
def load_user(id):
    return db.session.query(User).get(id)

with app.app_context():
    db.create_all()
    db.session.commit()

