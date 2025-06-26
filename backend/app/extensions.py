from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate, ValidationError
# from flask_migrate import Migrate 

db = SQLAlchemy()
ma = Marshmallow()
#migrate = Migrate()
# add celery extension here