"""Flask configuration."""

import os

SECRET_KEY = os.urandom(24)
MAX_CONTENT_LENGTH = 10 * 1024 * 1024
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
SESSION_TYPE = 'sqlalchemy'
SESSION_PERMANENT = True
ENV="DEV"
cwd = os.getcwd()
UPLOAD_FOLDER = f'{cwd}/src/static/uploads' 
SALT = b'\t\xc0\x06@\x050w\n\xd8~\x94\xb11\xfaOV' # different in production