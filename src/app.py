"""Bundle all sections and expose the Flask APP"""

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile('./config.py')

db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db

Session(app)

db.create_all()
db.session.commit()

from .modules import *
from .routes import *
