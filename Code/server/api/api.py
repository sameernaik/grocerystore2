# api.api.py
from api.category import *
from api.cart import *
from api.product import *
from api.manager import *
from api.approval import *
from api.order import OrderInfoResource, OrderProductInfoResource
from api.purchaseorder import *
from approvalsService import ApprovalsService
from sqlalchemy import func
from enum import Enum
from summary import defineSummaryRoutes
from flask import jsonify, request, current_app
from models import User, Manager, db, PurchaseOrderStatus, Product, Category
from flask_jwt_extended import JWTManager, create_access_token
from datetime import datetime, timedelta
from collections import OrderedDict
from sqlalchemy.exc import IntegrityError

import time
from cache_utils import cache, clear_cache


def defineAPIRoutes(app):
    app.config["JWT_SECRET_KEY"] = "Gurukrupa"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # expires after 1 hour
    api = Api(app)
    jwt = JWTManager(app)

    api.add_resource(CategoryAPI, "/api/category", "/api/category/<int:id>")
    api.add_resource(CartResource, "/api/cart/<int:cart_id>", "/api/cart")
    api.add_resource(CartItemResource, "/api/cart-item/<int:cart_item_id>")
    api.add_resource(CartItemsResource, "/api/cart-items")

    api.add_resource(PurchaseOrderResource, "/api/orders", "/api/orders/<int:order_id>")
    api.add_resource(
        PurchaseOrderItemListResource,
        "/api/purchase-order-item",
        "/api/purchase-order-items/<int:order_id>",
    )
    api.add_resource(UserOrdersResource, "/api/user-orders/<int:user_id>")

    api.add_resource(ProductResource, "/api/product/<int:product_id>")
    api.add_resource(ProductListResource, "/api/products")
    api.add_resource(ManagerUserResource, "/api/managers")
    api.add_resource(
        StoreManagerProductListResource, "/api/storemanager/<int:manager_id>/products"
    )
    api.add_resource(
        StoreManagerCategoryListResource,
        "/api/storemanager/<int:manager_id>/categories",
    )
    api.add_resource(ApprovalResource, "/api/approvals", endpoint="approvals")
    api.add_resource(
        ApprovalResource, "/api/approvals/<int:approval_id>", endpoint="approval"
    )

    api.add_resource(OrderInfoResource, "/api/order-info/<int:order_id>")
    api.add_resource(
        OrderProductInfoResource, "/api/order-products-info/<int:order_id>"
    )
    # defineSummaryRoutes(app)

    # Fixing swagger.json request blocked due to CORS  Start
    CORS(app, support_credentials=True)
    # cors = CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8080"], "methods": ["GET", "POST","PUT","DELETE"], "support_credentials": True}})

    # @app.route("/api/login")
    # @cross_origin(supports_credentials=True)
    # def login():
    #    return jsonify({"success": "ok", "name": "vrunda sameer naik"})

    # Fixing swagger.json request blocked due to CORS  End

    @app.route("/api/login", methods=("POST",))
    def login():
        data = request.get_json()
        user = User.authenticate(**data)

        if not user:
            return (
                jsonify({"error": "Invalid credentials", "authenticated": False}),
                401,
            )

        manager_id = -1
        if user.role == "USER":
            manager_id = -1
        elif user.role == "STORE_MANAGER":
            manager = Manager.query.filter(Manager.userid == user.id).first()
            if manager.approved == 1:
                manager_id = manager.id
            elif manager.approved == 0:
                return (
                    jsonify(
                        {"error": "Store Manager not approved.", "authenticated": False}
                    ),
                    401,
                )
        elif user.role == "ADMIN":
            manager_id = 0
        user_info = {
            "user_id": user.id,
            "role": user.role,
            "username": user.username,
            "manager_id": manager_id,
        }

        token = create_access_token(identity=user.id)
        print(token)
        print("Secret key", app.config["JWT_SECRET_KEY"])
        try:
            user.last_login = datetime.now()
            db.session.commit()
        except Exception as e:
            print(e)

        return jsonify({"token": token, "user_info": user_info}), 200

    @app.route("/api/register", methods=("POST",))
    def register():
        try:
            data = request.get_json()
            user = User(**data)
            db.session.add(user)
            db.session.commit()
            if user.role == "STORE_MANAGER":
                manager = Manager(userid=user.id)
                db.session.add(manager)
                db.session.commit()
                # commit data in DB with default value of approval status 0 (Unapproved) and request approval from Admin.
                message = f"Store Manager '{user.username}' has requested registration approval."
                ApprovalsService.create_approval(
                    requester_id=manager.id,
                    approval_type="STORE_MANAGER",
                    target_id=manager.id,
                    task="EDIT",
                    modification=1,
                    status="NEW",
                    message=message,
                )

            return jsonify(user.to_dict()), 201
        except IntegrityError as e:
            db.session.rollback()
            if "UNIQUE constraint failed: user.username" in str(e):
                return jsonify({"error": "Username or email is already in use."}), 400
        except Exception as e:
            print(e)

    @app.route("/api/catalog", methods=("GET",))
    @cache.cached(timeout=600)  # Timeout in seconds
    def catalog():
        print("catalog called ")
        time.sleep(1)
        try:
            cache_key = (request.endpoint, request.url)
            print("Cache Key:", cache_key)
            dbCategoryList = Category.query.all()
            categoryProductDict = OrderedDict()
            for category in dbCategoryList:
                print(category.id)
                dbProductList = Product.query.filter(
                    Product.categoryid == category.id
                ).all()
                print(dbProductList)
                product_list_dict = [product.to_dict() for product in dbProductList]
                # print(product_list_dict)
                categoryProductDict[category.id] = product_list_dict
            # print(categoryProductDict)
            return jsonify(categoryProductDict)
        except Exception as e:
            print("Exception ", e)

    @app.route("/api/product-catalog", methods=("GET",))
    @cache.cached(timeout=600)  # Timeout in seconds
    def product_catalog_cached():
        print("Cached product catalog called ")
        time.sleep(1)
        try:
            cache_key = (request.endpoint, request.url)
            print("Cache Key:", cache_key)
            dbCategoryList = Category.query.all()
            categoryProductDict = OrderedDict()
            for category in dbCategoryList:
                print(category.id)
                dbProductList = Product.query.filter(
                    Product.categoryid == category.id
                ).all()
                print(dbProductList)
                product_list_dict = [product.to_dict() for product in dbProductList]
                # print(product_list_dict)
                categoryProductDict[category.id] = product_list_dict
            # print(categoryProductDict)
            return jsonify(categoryProductDict)
        except Exception as e:
            print("Exception ", e)

    @app.route("/api/clear-cache")
    def clear_cache1():
        clear_cache()
        print("cache cleared successfully")
        return "Cache cleared successfully"

    @app.route("/api/generate-graphs")
    def generate_graphs():
        try:
            app.generateTopNProductsGraph("top_10_product_quantity.png", 10)
            app.generateTopNCategorywiseProductsGraph(
                "top_10_categorywise_product.png", 10
            )
            app.generateDayOfWeekVsOrdersGraph("dayOfWeekWiseOrders.png")
            app.generateModeOfPaymentTrendGraph("paymentModeTrend.png")

            return jsonify(
                {"success": True, "message": "Graphs generated successfully"}
            )
        except Exception as e:
            return jsonify(
                {"success": False, "message": f"Error generating graphs: {str(e)}"}
            )

    @app.route("/api/buy-again")
    @jwt_required()
    def computeBuyAgainProductList():
        current_user = get_jwt_identity()
        print("current_user", current_user)
        buyAgainProductList = []
        userId = current_user
        # session_id=session.get('shopping-session-id',None)
        if userId != None:
            dbProductIdTupleList = (
                db.session.query(Product.id)
                .filter(Product.id == PurchaseOrderItem.product_id)
                .filter(PurchaseOrder.user_id == userId)
                .filter(PurchaseOrderItem.order_id == PurchaseOrder.id)
                .filter(PurchaseOrder.status == PurchaseOrderStatus.SUCCESS)
                .filter(PurchaseOrder.created_at.between("2023-07-29", "2024-12-31"))
                .group_by(PurchaseOrderItem.product_id)
                .order_by(func.sum(PurchaseOrderItem.quantity).desc())
                .limit(4)
                .all()
            )
            dbProductIdList = []
            for productIdTuple in dbProductIdTupleList:
                dbProductIdList.append(productIdTuple[0])

            print("### BuyAgain db Product ID List", dbProductIdList)
            buyAgainProductList = Product.query.filter(
                Product.id.in_(dbProductIdList)
            ).all()

            product_list_dict = [product.to_dict() for product in buyAgainProductList]

            if len(product_list_dict) > 0:
                print("### BuyAgain Product List", product_list_dict)
            else:
                print("### Buy Again Product List not found.")
        return jsonify(product_list_dict)
