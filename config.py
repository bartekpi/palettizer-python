import os
import secrets

FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', secrets.token_urlsafe(32))
N_CLUSTERS = 8
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
APP_NAME = 'pltzr-python'
APP_TITLE = 'plttzrrrrr'
APP_REPO = 'https://github.com/bartekpi/palettizer-python'
