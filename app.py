from flask import Flask, g
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_script import Manager
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.before_request
def before_request():
    g.user = current_user 