from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from flask_admin import Admin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chamados.db"
app.config["SECRET_KEY"] = "a3190c71717b80582c2b580d8bc02528"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

admin = Admin(app, name='Painel de Controle', template_mode='bootstrap3')

from aplicacao import routes
