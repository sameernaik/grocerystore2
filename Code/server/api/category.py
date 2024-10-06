from flask_restful import Resource, Api, fields, marshal_with, reqparse, abort
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from models import db, Category, Product, Manager, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from approvalsService import ApprovalsService

# from datetime import datetime
from api.validation import NotFoundError, InternalServerError

category_output_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "owner": fields.Integer,
    "created_at": fields.String,
    "modified_at": fields.String,
}


create_category_parser = reqparse.RequestParser()
create_category_parser.add_argument("name")
create_category_parser.add_argument("owner")
create_category_parser.add_argument("category_description")

update_category_parser = reqparse.RequestParser()
update_category_parser.add_argument("name")
update_category_parser.add_argument("owner")
# update_category_parser.add_argument('created_at')
# update_category_parser.add_argument('modified_at')


class CategoryAPI(Resource):
    @marshal_with(category_output_fields)
    def get(self, id=None):
        try:
            if id:
                # If an ID is provided, return the specific category
                dbcategory = Category.query.filter(Category.id == id).first()
                if dbcategory:
                    return dbcategory
                else:
                    raise NotFoundError("Category not found")
            else:
                # If no ID is provided, return all categories
                dbcategories = Category.query.all()
                return dbcategories

        except NotFoundError as e:
            raise
        except Exception as e:
            raise InternalServerError(str(e))

    @jwt_required()
    @marshal_with(category_output_fields)
    def put(self, id):
        current_user = get_jwt_identity()
        print("current_user", current_user)
        if current_user == 1:
            print("Admin User")
            try:
                args = update_category_parser.parse_args()
                category_name1 = args.get("name", None)
                category_owner = args.get("owner", None)
                # category_created_at=args.get("created_at",None)
                # category_modified_at=args.get("modified_at",None)

                dbcategory = Category.query.filter(Category.id == id).first()
                if dbcategory:
                    dbcategory.name = category_name1
                    dbcategory.owner = category_owner
                    # if category_created_at:
                    #     dbcategory.created_at=datetime.strptime(category_created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
                    # if category_modified_at:
                    #    dbcategory.modified_at=datetime.strptime(category_modified_at,'%Y-%m-%dT%H:%M:%S.%fZ')
                    db.session.add(dbcategory)
                    db.session.commit()
                    return dbcategory, 200
                else:
                    raise NotFoundError("category not found")
            except NotFoundError:
                raise
            except Exception as e:
                raise InternalServerError(str(e))
        else:
            # Store Manager User
            try:
                args = update_category_parser.parse_args()
                category_name1 = args.get("name", None)
                manager = Manager.query.filter(Manager.userid == current_user).first()
                if manager:
                    user = User.query.filter(User.id == current_user).first()
                    username = user.username
                    dbcategory = Category.query.filter(Category.id == id).first()
                    categoryname = dbcategory.name
                    message = f"Store Manager '{username}' has requested Editing of category name from '{categoryname}' to '{category_name1}'."
                    ApprovalsService.create_approval(
                        requester_id=manager.id,
                        approval_type="CATEGORY",
                        target_id=id,
                        task="EDIT",
                        modification=category_name1,
                        status="NEW",
                        message=message
                    )
                    response = make_response(
                        jsonify(
                            {"message": "Edit Category request submitted successfully"}
                        ),
                        200,
                    )
                    return response
                else:
                    response = make_response(
                        jsonify(
                            {
                                "message": "Request submission failed because manager not found for userid "
                                + current_user
                            }
                        ),
                        400,
                    )
                    return response
            except Exception as e:
                raise InternalServerError(str(e))

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        print("current_user", current_user)
        if current_user == 1:
            print("Admin User")
            try:
                dbcategory = Category.query.filter(Category.id == id).first()
                print("dbcategory ", dbcategory, id)
                if dbcategory is None:
                    raise NotFoundError("category not found")
                else:
                    Product.query.filter(Product.categoryid == id).delete()
                    Category.query.filter(Category.id == id).delete()
                    db.session.commit()
                    return "Successfully Deleted", 200
            except NotFoundError:
                raise
            except Exception as e:
                raise InternalServerError(str(e))
        else:
            # Manager User
            try:
                manager = Manager.query.filter(Manager.userid == current_user).first()
                if manager:
                    user = User.query.filter(User.id == current_user).first()
                    username = user.username
                    dbcategory = Category.query.filter(Category.id == id).first()
                    categoryname = dbcategory.name
                    message = f"Store Manager '{username}' has requested Deletion of category '{categoryname}'."
                    ApprovalsService.create_approval(
                        requester_id=manager.id,
                        approval_type="CATEGORY",
                        target_id=id,
                        task="DELETE",
                        modification="",
                        status="NEW",
                        message=message,
                    )
                    response = make_response(
                        jsonify(
                            {
                                "message": "Delete Category request submitted successfully"
                            }
                        ),
                        200,
                    )
                    return response
                else:
                    response = make_response(
                        jsonify(
                            {
                                "message": "Delete Category request submission failed because manager not found for userid "
                                + current_user
                            }
                        ),
                        400,
                    )
                    return response

            except Exception as e:
                raise InternalServerError(str(e))

    @jwt_required()
    @marshal_with(category_output_fields)
    def post(self):
        current_user = get_jwt_identity()
        print("current_user", current_user)
        if current_user == 1:
            print("Admin User")
            try:
                args = create_category_parser.parse_args()
                category_name = args.get("name", None)
                category_owner = args.get("owner", None)

                dbcategory = Category.query.filter(
                    Category.name == category_name
                ).first()
                if dbcategory:
                    return "category_code already exists", 409
                else:
                    new_category = Category(name=category_name, owner=category_owner)
                    db.session.add(new_category)
                    db.session.commit()
                    print("#######", category_name, category_owner)
                    return new_category, 201
            except Exception as e:
                raise InternalServerError(str(e))
        else:
            # Manager User
            try:
                manager = Manager.query.filter(Manager.userid == current_user).first()
                args = create_category_parser.parse_args()
                category_name = args.get("name", None)
                if manager:
                    user = User.query.filter(User.id == current_user).first()
                    username = user.username
                    message = f"Store Manager '{username}' has requested Addition of new category '{category_name}'."
                    ApprovalsService.create_approval(
                        requester_id=manager.id,
                        approval_type="CATEGORY",
                        target_id=-1,
                        task="CREATE",
                        modification=category_name,
                        status="NEW",
                        message=message,
                    )
                    response = make_response(
                        jsonify(
                            {
                                "message": "Delete Category request submitted successfully"
                            }
                        ),
                        200,
                    )
                    return response
                else:
                    response = make_response(
                        jsonify(
                            {
                                "message": "Delete Category request submission failed because manager not found for userid "
                                + current_user
                            }
                        ),
                        400,
                    )
                    return response

            except Exception as e:
                raise InternalServerError(str(e))


class StoreManagerCategoryListResource(Resource):
    @marshal_with(category_output_fields)
    @jwt_required()
    def get(self, manager_id):
        current_user = get_jwt_identity()
        print("current_user", current_user)
        if current_user == 1:
            # Admin user. Return all products.
            dbCategoryList = Category.query.order_by(Category.id).all()
            return dbCategoryList
        else:
            manager = Manager.query.filter(Manager.userid == current_user).first()
            print("manager", manager)
            print("(manager.id == manager_id)", (manager.id == manager_id))
            if manager and (manager.id == manager_id):
                print("manager.id ", manager.id)
                # Valid request manager id in get request and identified through token is same.
                dbCategoryList = Category.query.filter(
                    Category.owner == manager_id
                ).all()
                return dbCategoryList
            else:
                abort(401, message="Unauthorized request")
