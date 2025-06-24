from marshmallow import Schema, fields
from app.extensions import ma
from app.models.category import Category


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)