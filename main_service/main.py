from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import *
import os
from flask_cors import CORS

app = None
def create_app():
    app=Flask(__name__)
    print("starting local development")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app=create_app()
CORS(app)

if not os.path.exists(os.path.join(app.instance_path, 'database.sqlite3')):
    db.create_all()

from application.api import *

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
