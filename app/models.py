# mm-inventory/app/models.py

from . import db  # Import the db instance from __init__.py


class ProductItem(db.Model):
    __tablename__ = 'productitem'
    id = db.Column(db.Integer, primary_key=True)
    productid = db.Column(db.Integer, nullable=False)
    storeid = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<ProductItem {self.productid}, {self.storeid}, Price: {self.price}, Stock: {self.stock}>"
