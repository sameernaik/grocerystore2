from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required
from models import db, Cart, CartItem
from datetime import datetime


class CartResource(Resource):
    def get(self, cart_id):
        # Retrieve cart information by ID
        cart = Cart.query.get(cart_id)
        if cart:
            return {
                "id": cart.id,
                "user_id": cart.user_id,
                "total": cart.total,
                "created_at": cart.created_at.isoformat(),
                "modified_at": cart.modified_at.isoformat(),
                "status": cart.status,
                "apply_promo_code": cart.apply_promo_code,
            }
        else:
            return {"message": "Cart not found"}, 404

    @jwt_required()
    def post(self):
        # Create a new cart
        parser = reqparse.RequestParser()
        parser.add_argument(
            "user_id", type=int, required=True, help="user_id is required"
        )
        parser.add_argument(
            "total", type=float, required=True, help="total is required"
        )
        # Add other required parameters for creating a cart
        args = parser.parse_args()

        new_cart = Cart(
            user_id=args["user_id"],
            total=args[
                "total"
            ],  # Set initial total to 0 or calculate based on cart items
            # created_at=datetime.now(),
            # modified_at=datetime.now(),
            status=1,  # Set default status (you may need to adjust this)
            apply_promo_code=0,  # Set default promo code status
        )

        db.session.add(new_cart)
        db.session.commit()

        return {"message": "Cart created successfully", "cart_id": new_cart.id}, 201

    @jwt_required()
    def put(self, cart_id):
        # Update cart information
        parser = reqparse.RequestParser()
        parser.add_argument("total", type=int)
        parser.add_argument("status", type=int)
        parser.add_argument("apply_promo_code", type=int)
        # Add other parameters you want to update

        args = parser.parse_args()

        cart = Cart.query.get(cart_id)
        if not cart:
            return {"message": "Cart not found"}, 404

        # Update only the provided fields
        if "total" in args:
            cart.total = args["total"]
        if "status" in args:
            cart.status = args["status"]
        if "apply_promo_code" in args:
            cart.apply_promo_code = args["apply_promo_code"]

        cart.modified_at = datetime.now()

        db.session.commit()

        return {"message": "Cart updated successfully"}, 200

    @jwt_required()
    def delete(self, cart_id):
        # Delete cart by ID
        cart = Cart.query.get(cart_id)
        if cart:
            db.session.delete(cart)
            db.session.commit()
            return {"message": "Cart deleted successfully"}, 200
        else:
            return {"message": "Cart not found"}, 404


# Resource for CartItem
class CartItemResource(Resource):
    def get(self, cart_item_id):
        cart_item = CartItem.query.get(cart_item_id)
        if cart_item:
            return {
                "id": cart_item.id,
                "cart_id": cart_item.cart_id,
                "product_id": cart_item.product_id,
                "quantity": cart_item.quantity,
                "price": cart_item.price,
                "discount": cart_item.discount,
                "discounted_price": cart_item.discounted_price,
                "status": cart_item.status,
                "created_at": cart_item.created_at.isoformat(),
                "modified_at": cart_item.modified_at.isoformat(),
            }
        else:
            return {"message": "CartItem not found"}, 404

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "cart_id", type=int, required=True, help="Cart ID is required"
        )
        parser.add_argument(
            "product_id", type=int, required=True, help="Product ID is required"
        )
        parser.add_argument("quantity", type=int, default=0)
        parser.add_argument("price", type=float, default=0.0)
        parser.add_argument("discount", type=float, default=0.0)
        args = parser.parse_args()

        new_cart_item = CartItem(
            cart_id=args["cart_id"],
            product_id=args["product_id"],
            quantity=args["quantity"],
            price=args["price"],
            discount=args["discount"],
            discounted_price=args["price"] * (100 - args["discount"]) / 100,
            created_at=datetime.now(),
            modified_at=datetime.now(),
        )

        db.session.add(new_cart_item)
        db.session.commit()

        return {
            "message": "CartItem created successfully",
            "cart_item_id": new_cart_item.id,
        }, 201

    @jwt_required()
    def put(self, cart_item_id):
        cart_item = CartItem.query.get(cart_item_id)
        if cart_item:
            parser = reqparse.RequestParser()
            parser.add_argument("quantity", type=int)
            parser.add_argument("price", type=float)
            parser.add_argument("discount", type=float)
            args = parser.parse_args()

            if args["quantity"] is not None:
                cart_item.quantity = args["quantity"]
            if args["price"] is not None:
                cart_item.price = args["price"]
            if args["discount"] is not None:
                cart_item.discount = args["discount"]
                cart_item.discounted_price = (
                    cart_item.price * (100 - cart_item.discount) / 100
                )

            cart_item.modified_at = datetime.now()
            db.session.commit()

            return {"message": "CartItem updated successfully"}
        else:
            return {"message": "CartItem not found"}, 404

    @jwt_required()
    def delete(self, cart_item_id):
        cart_item = CartItem.query.get(cart_item_id)
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return {"message": "CartItem deleted successfully"}
        else:
            return {"message": "CartItem not found"}, 404


# class to get cart-items for a particular session_id
class CartItemsResource(Resource):
    # GET /cart-items?session_id=123
    def get(self):
        session_id = request.args.get("session_id")
        if not session_id:
            return {"message": "session_id is required"}, 400

        cart_items = CartItem.query.filter_by(session_id=session_id).all()

        if not cart_items:
            return {"message": "No cart items found for the given session_id"}, 404

        cart_items_data = []
        for item in cart_items:
            cart_items_data.append(
                {
                    "id": item.id,
                    "session_id": item.session_id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price,
                    "discount": item.discount,
                    "discounted_price": item.discounted_price,
                    "status": item.status,
                    "created_at": item.created_at.isoformat(),
                    "modified_at": item.modified_at.isoformat(),
                }
            )

        return {"cart_items": cart_items_data}, 200

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("session_id", type=int, required=True, help="Session ID is required")
        parser.add_argument("product_id", type=int, required=True, help="Product ID is required")
        parser.add_argument("quantity", type=int, default=0)
        parser.add_argument("price", type=int, default=0)
        parser.add_argument("discount", type=int, default=0)
        args = parser.parse_args()

        # Calculate discounted_price based on price and discount
        discounted_price = args["price"] * (100 - args["discount"]) / 100

        new_cart_item = CartItem(
            session_id=args["session_id"],
            product_id=args["product_id"],
            quantity=args["quantity"],
            price=args["price"],
            discount=args["discount"],
            discounted_price=discounted_price,
            status=1,  # Assuming default status is 1 (Available)
            created_at=datetime.now(),
            modified_at=datetime.now(),
        )

        try:
            db.session.add(new_cart_item)
            db.session.commit()
            return {"message": "CartItem created successfully", "cart_item_id": new_cart_item.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error creating CartItem: {str(e)}"}, 500

    @jwt_required()
    def put(self):
        session_id = request.args.get("session_id")
        if not session_id:
            return {"message": "session_id is required"}, 400

        cart_items_data = request.json.get("cart_items")
        if not cart_items_data or not isinstance(cart_items_data, list):
            return {"message": "Invalid or missing cart_items data in the request"}, 400

        for data in cart_items_data:
            item_id = data.get("id")
            quantity = data.get("quantity")
            price = data.get("price")
            discount = data.get("discount")

            if item_id:
                cart_item = CartItem.query.filter_by(
                    id=item_id, session_id=session_id
                ).first()
                if cart_item:
                    cart_item.quantity = (
                        quantity if quantity is not None else cart_item.quantity
                    )
                    cart_item.price = price if price is not None else cart_item.price
                    cart_item.discount = (
                        discount if discount is not None else cart_item.discount
                    )
                    cart_item.modified_at = datetime.now()
                    db.session.commit()

        return {"message": "Cart items updated successfully"}, 200

    @jwt_required()
    def delete(self):
        session_id = request.args.get("session_id")
        if not session_id:
            return {"message": "session_id is required"}, 400

        cart_items_ids = request.json.get("cart_items_ids")
        if not cart_items_ids or not isinstance(cart_items_ids, list):
            return {
                "message": "Invalid or missing cart_items_ids data in the request"
            }, 400

        for item_id in cart_items_ids:
            cart_item = CartItem.query.filter_by(
                id=item_id, session_id=session_id
            ).first()
            if cart_item:
                db.session.delete(cart_item)
                db.session.commit()

        return {"message": "Cart items deleted successfully"}, 200
