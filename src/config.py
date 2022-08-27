"""Flask configuration."""

import os

SECRET_KEY = os.urandom(24)
MAX_CONTENT_LENGTH = 10 * 1024 * 1024
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
SESSION_TYPE = 'sqlalchemy'
SESSION_PERMANENT = True
