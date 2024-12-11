import os
class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
    DEBUG = True

ENTITIES_SERVICE_URL = "http://entities-service:5001"
RELATIONSHIPS_SERVICE_URL = "http://relations-service:5002"
LLAMA_URL = "host.docker.internal"

# ENTITIES_SERVICE_URL = "http://localhost:5001"
# RELATIONSHIPS_SERVICE_URL = "http://localhost:5002"
# LLAMA_URL = "localhost"
