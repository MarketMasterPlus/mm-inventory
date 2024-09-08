# mm-inventory/app/api/routes.py
from flask import request
from flask_restx import Resource, fields, Namespace, reqparse
from ..models import db, ProductItem
from ..schemas import ProductItemSchema
import requests
import os

def init_routes(api):
    # Define namespaces
    inventory_ns = Namespace('productitems', description='Product item operations')
    api.add_namespace(inventory_ns, path='/mm-inventory')

    productitem_model = api.model('ProductItem', {
        'id': fields.Integer(readOnly=True, description='The unique identifier of a product item'),
        'productid': fields.Integer(required=True, description='Product identifier'),
        'storeid': fields.Integer(required=True, description='Store identifier'),
        'price': fields.Float(required=True, description='Price of a single unit of the product'),
        'stock': fields.Integer(required=True, description='Number of units in stock')
    })

    # Single query parser definition
    query_parser = reqparse.RequestParser()
    query_parser.add_argument('name', type=str, help='Filter by product name')
    query_parser.add_argument('category', type=str, help='Filter by product category ID')
    query_parser.add_argument('description', type=str, help='Filter by product description')
    query_parser.add_argument('brand', type=str, help='Filter by product brand')



    @inventory_ns.route('/')
    class ProductItemList(Resource):
        @inventory_ns.expect(query_parser)  # Use expect to add the parser to Swagger UI
        @inventory_ns.doc('list_productitems')
        @inventory_ns.marshal_list_with(productitem_model)
        def get(self):
            """
            List all product items or search by specified attributes.
            Query parameters for filtering by name, category, description, and brand are accepted.
            """
            args = query_parser.parse_args()  # Use parsed arguments
            product_ids = fetch_product_ids_matching_filters(args)
            if product_ids:
                productitems = ProductItem.query.filter(ProductItem.productid.in_(product_ids)).all()
            else:
                productitems = ProductItem.query.all()
            return productitems

        @inventory_ns.doc('create_productitem')
        @inventory_ns.expect(productitem_model)
        @inventory_ns.marshal_with(productitem_model, code=201)
        def post(self):
            data = request.json
            productitem = ProductItem(**data)
            db.session.add(productitem)
            db.session.commit()
            return productitem, 201

    @inventory_ns.route('/<int:id>')
    class ProductItemDetail(Resource):
        @inventory_ns.doc('get_productitem')
        @inventory_ns.marshal_with(productitem_model)
        def get(self, id):
            productitem = ProductItem.query.get_or_404(id)
            return productitem

        @inventory_ns.doc('update_productitem')
        @inventory_ns.expect(productitem_model)
        @inventory_ns.marshal_with(productitem_model)
        def put(self, id):
            productitem = ProductItem.query.get_or_404(id)
            data = request.json
            for key, value in data.items():
                setattr(productitem, key, value)
            db.session.commit()
            return productitem

        @inventory_ns.doc('delete_productitem')
        @inventory_ns.response(204, 'Product item deleted')
        def delete(self, id):
            productitem = ProductItem.query.get_or_404(id)
            db.session.delete(productitem)
            db.session.commit()
            return '', 204

    @inventory_ns.route('/city/<string:city>')
    @inventory_ns.doc('list_productitems_by_city')
    class ProductItemsByCity(Resource):
        @inventory_ns.expect(query_parser)  # Use expect to add the parser to Swagger UI
        @inventory_ns.marshal_list_with(productitem_model)
        def get(self, city):
            store_ids = get_store_ids_by_city(city)
            args = query_parser.parse_args()
            product_ids = fetch_product_ids_matching_filters(args)
            if store_ids and product_ids:
                productitems = ProductItem.query.filter(
                    ProductItem.storeid.in_(store_ids),
                    ProductItem.productid.in_(product_ids)
                ).all()
            else:
                productitems = []
            return productitems

    @inventory_ns.route('/store/<int:store_id>')
    @inventory_ns.doc('list_productitems_by_store')
    class ProductItemsByStore(Resource):
        @inventory_ns.expect(query_parser)  # Use expect to add the parser to Swagger UI
        @inventory_ns.marshal_list_with(productitem_model)
        def get(self, store_id):
            product_ids = fetch_product_ids_matching_filters(request.args)
            if product_ids:
                productitems = ProductItem.query.filter(
                    ProductItem.storeid == store_id,
                    ProductItem.productid.in_(product_ids)
                ).all()
            else:
                productitems = []
            return productitems

#
# def fetch_product_ids_matching_filters(filters):
#     """Fetch product IDs from mm-product that match the given filters"""
#     query_params = {key: val for key, val in filters.items() if key in ['name', 'category', 'description', 'brand']}
#     response = requests.get(f"{os.getenv('MM_PRODUCT_URL', 'http://mm-product:5704')}/mm-product", params=query_params)
#     if response.status_code == 200:
#         products = response.json()
#         return [product['id'] for product in products]
#     return []

def fetch_product_ids_matching_filters(filters):
    """Fetch product IDs from mm-product that match the given filters"""
    response = requests.get(f"{os.getenv('MM_PRODUCT_URL', 'http://mm-product:5704')}/mm-product", params=filters)
    if response.status_code == 200:
        products = response.json()
        return [product['id'] for product in products]
    return []


def get_store_ids_by_city(city):
    """Fetch store IDs from mm-store service that are located in a specified city"""
    store_url = f"{os.getenv('MM_STORE_URL', 'http://mm-store:5701')}/mm-store/city/{city}"
    response = requests.get(store_url)
    if response.status_code == 200:
        stores = response.json()
        return [store['id'] for store in stores]
    return []

