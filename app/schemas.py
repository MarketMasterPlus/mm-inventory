# mm-inventory/app/schemas.py
from flask_marshmallow import Marshmallow
from .models import ProductItem

ma = Marshmallow()


class ProductItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductItem
        load_instance = True  # Optional: if true, deserialization will create model instances.
