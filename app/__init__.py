from flask import Flask
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.sqlalchemy import SQLAlchemy
import logging
from flask_mail import Mail


app = Flask(__name__)
api = Api(app)

#app.config.from_object('config.ProductionConfig')
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

mail = Mail(app)


from app import views, models, forms, rest
api.add_resource(rest.SensorAPI, '/rest/sensor/<int:id>', endpoint='sensor')
api.add_resource(rest.MedicionAPI, '/rest/medicion/<int:id>', endpoint='medicion')

