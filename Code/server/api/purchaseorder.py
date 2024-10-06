from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from datetime import datetime, timedelta
from models import db, PurchaseOrder, PurchaseOrderItem


class PurchaseOrderResource(Resource):
    def get(self, order_id):
        order = PurchaseOrder.query.get_or_404(order_id)
        return {
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status.name,
            "created_at": order.created_at,
            "total": order.total,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price,
                    "discount": item.discount,
                }
                for item in order.items
            ],
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True)
        parser.add_argument("shipping_charges", type=int, required=True)
        parser.add_argument("total", type=int, required=True)

        parser.add_argument("session_id", type=int, required=True)
        parser.add_argument("status", required=True)

        # Add other required fields
        args = parser.parse_args()

        new_order = PurchaseOrder(
            user_id=args["user_id"],
            shipping_charges=args["shipping_charges"],
            total=args["total"],
            session_id=args["session_id"],
            status=args["status"]
            # Set other fields accordingly
        )

        db.session.add(new_order)
        db.session.commit()

        return {
            "id": new_order.id,
            "user_id": new_order.user_id,
            "status": new_order.status.value,
            "created_at": new_order.created_at.isoformat(),
        }


class PurchaseOrderItemListResource(Resource):
    def get(self, order_id):
        items = PurchaseOrderItem.query.filter_by(order_id=order_id).all()
        return [
            {
                "id": item.id,
                "order_id": item.order_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price,
                "discount": item.discount,
                "discounted_price": item.discounted_price,
                "created_at": item.created_at,
                "modified_at": item.modified_at,
            }
            for item in items
        ]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("order_id", type=int, required=True)
        parser.add_argument("product_id", type=int, required=True)
        parser.add_argument("quantity", type=int, required=True)
        parser.add_argument("price", type=int, required=True)
        parser.add_argument("discount", type=int, required=True)
        args = parser.parse_args()

        new_item = PurchaseOrderItem(
            order_id=args["order_id"],
            product_id=args["product_id"],
            quantity=args["quantity"],
            price=args["price"],
            discount=args["discount"],
        )

        db.session.add(new_item)
        db.session.commit()

        return {
            "id": new_item.id,
            "order_id": new_item.order_id,
            "product_id": new_item.product_id,
            "quantity": new_item.quantity,
            "price": new_item.price,
            "discount": new_item.discount,
        }


class UserOrdersResource(Resource):
    def get(self, user_id):
        orders = PurchaseOrder.query.filter_by(user_id=user_id).all()

        user_orders = [
            {
                "id": order.id,
                "status": order.status.name,
                "created_at": order.created_at.isoformat(),
                "total": order.total,
            }
            for order in orders
        ]

        return user_orders
