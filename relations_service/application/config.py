import os
class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
    DEBUG = True

# Base URLs for other services
# ENTITIES_SERVICE_URL = "http://entities-service:5001/entities/hello"
# ENTITIES_SERVICE_URL = "http://localhost:5001/"
ENTITIES_SERVICE_URL = "http://entities-service:5001/"

# RELATIONSHIPS_SERVICE_URL = "http://localhost:5002/relationships/hello"
# ANOMALIES_SERVICE_URL = "http://localhost:5003/anomalies/hello"