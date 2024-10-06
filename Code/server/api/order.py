from flask import Flask,jsonify
from flask_restful import Api, Resource, reqparse
from models import db, PurchaseOrder, User, PurchaseOrderItem, Product
from orderService import OrderService

class OrderInfoResource(Resource):
    def get(self, order_id):
        order_info = OrderService.getOrderInfo(order_id)
        if order_info:
            return {"order_info": order_info}
        else:
            return {"error": "Order not found"}, 404


class OrderProductInfoResource(Resource):
    def get(self, order_id):
        order_products_info = OrderService.getOrderProductsInfo(order_id)
        if order_products_info:
            serialized_products = [
                product for product in order_products_info
            ]
            return jsonify(order_products_info)
        else:
            return {"error": "Order products not found"}, 404



