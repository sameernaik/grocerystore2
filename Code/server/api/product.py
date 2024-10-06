# api.product.py
from flask_restful import Resource, Api, fields, marshal_with, abort
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from models import db, Category, Product, Manager
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from cache_utils import clear_cache

from api.validation import NotFoundError, InternalServerError

# Define the fields you want to expose in the API response
product_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "imagename": fields.String,
    "description": fields.String,
    "categoryid": fields.Integer,
    "sell_quantity": fields.Integer,
    "sell_unit": fields.String,
    "stock_quantity": fields.Integer,
    "stock_unit": fields.String,
    "price": fields.Integer,
    "discount": fields.Integer,
    "discounted_price": fields.Float(
        attribute=lambda x: x.price * (100 - x.discount) / 100
        if x.discount is not None
        else x.price
    ),
    "available": fields.Integer,
    "manufacturingdate": fields.String(attribute=lambda x: str(x.manufacturingdate)),
    "expirydate": fields.String(attribute=lambda x: str(x.expirydate)),
    "created_at": fields.String(attribute=lambda x: str(x.created_at)),
    "modified_at": fields.String(attribute=lambda x: str(x.modified_at)),
}


class ProductResource(Resource):
    @marshal_with(product_fields)
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return product

    @marshal_with(product_fields)
    @jwt_required()
    def put(self, product_id):
        product = Product.query.get_or_404(product_id)
        data = request.get_json()

        # Update product fields
        product.name = data.get("name", product.name)
        product.imagename = data.get("imagename", product.imagename)
        product.description = data.get("description", product.description)
        product.categoryid = data.get("categoryid", product.categoryid)
        product.sell_quantity = data.get("sell_quantity", product.sell_quantity)
        product.sell_unit = data.get("sell_unit", product.sell_unit)
        product.stock_quantity = data.get("stock_quantity", product.stock_quantity)
        product.stock_unit = data.get("stock_unit", product.stock_unit)
        product.price = data.get("price", product.price)
        product.discount = data.get("discount", product.discount)
        product.available = data.get("available", product.available)
        # Handle manufacturing date
        manufacturing_date_str = data.get("manufacturingdate")
        if manufacturing_date_str and manufacturing_date_str.lower() != "none":
            product.manufacturingdate = datetime.strptime(
                manufacturing_date_str, "%Y-%m-%d"
            ).date()
        else:
            product.manufacturingdate = None

        # Handle expiry date
        expiry_date_str = data.get("expirydate")
        if expiry_date_str and expiry_date_str.lower() != "none":
            product.expirydate = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        else:
            product.expirydate = None

        db.session.commit()
        print("Product Modified ", product_id)
        clear_cache()
        return product

    @jwt_required()
    def delete(self, product_id):
        # Soft delete if product_id was used
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        print("Product Deleted", product_id)
        clear_cache()
        return {"message": "Product deleted successfully"}


class ProductListResource(Resource):
    @marshal_with(product_fields)
    def get(self):
        products = Product.query.all()
        return products

    @jwt_required()
    @marshal_with(product_fields)
    def post(self):
        data = request.get_json()

        new_product = Product(
            name=data["name"],
            imagename=data.get("imagename"),
            description=data.get("description"),
            categoryid=data.get("categoryid"),
            sell_quantity=data.get("sell_quantity"),
            sell_unit=data.get("sell_unit"),
            stock_quantity=data.get("stock_quantity"),
            stock_unit=data.get("stock_unit"),
            price=data.get("price"),
            discount=data.get("discount"),
            available=data.get("available"),
            manufacturingdate=data.get("manufacturingdate"),
            expirydate=data.get("expirydate"),
        )

        db.session.add(new_product)
        db.session.commit()
        print("Product Added ")
        clear_cache()
        return new_product, 201


class StoreManagerProductListResource(Resource):
    @marshal_with(product_fields)
    @jwt_required()
    def get(self, manager_id):
        current_user = get_jwt_identity()
        print("current_user", current_user)
        if current_user == 1:
            # Admin user. Return all products.
            products = Product.query.order_by(Product.categoryid).all()
            return products
        else:
            manager = Manager.query.filter(Manager.userid == current_user).first()
            print("manager", manager)
            if manager:
                print("(manager.id == manager_id)", (manager.id == manager_id))
            if manager and (manager.id == manager_id):
                print("manager.id ", manager.id)
                # Valid request manager id in get request and identified through token is same.
                dbCategoryList = Category.query.filter(
                    Category.owner == manager_id
                ).all()
                dbCategoryIdList = []
                dbCategoriesDict = {}
                for category in dbCategoryList:
                    dbCategoryIdList.append(category.id)
                    dbCategoriesDict[category.id] = category.name
                print("dbCategoryIdList ", dbCategoryIdList)
                dbProductList = (
                    Product.query.filter(Product.categoryid.in_(dbCategoryIdList))
                    .order_by(Product.categoryid)
                    .all()
                )

                print("###products list", len(dbProductList))
                return dbProductList
            else:
                abort(401, message="Unauthorized request")
