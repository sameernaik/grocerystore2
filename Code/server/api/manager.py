from flask_restful import Resource
from flask import jsonify
from models import db, User, Manager


# Create a resource to handle the API endpoint
class ManagerUserResource(Resource):
    def get(self):
        # Query the database to get the desired information
        managers_users_data = (
            db.session.query(Manager.id, User.username).join(User).all()
        )
        result = [
            {"id":manager_id,"name":username} for manager_id, username in managers_users_data
        ]

        return jsonify(result)
