#!flask/bin/python
from migrate.versioning import api
from config import DevelopmentConfig as ambiente

 

from app import db
import os.path
db.create_all()
if not os.path.exists(ambiente.SQLALCHEMY_MIGRATE_REPO):
    api.create(ambiente.SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, ambiente.SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(ambiente.SQLALCHEMY_DATABASE_URI, ambiente.SQLALCHEMY_MIGRATE_REPO, api.version(ambiente.SQLALCHEMY_MIGRATE_REPO))