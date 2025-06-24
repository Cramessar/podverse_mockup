from marshmallow import Schema, fields
from app.extensions import ma
from app.models.medium import Medium


class MediumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Medium
        
medium_schema = MediumSchema()
mediums_schema = MediumSchema(many=True)
