from flask_restful import Resource, reqparse, fields, marshal_with
from flask import jsonify
from models import db, Approvals
from flask_jwt_extended import jwt_required, get_jwt_identity
from approvalsService import ApprovalsService


approval_fields = {
    "id": fields.Integer,
    "requester_id": fields.Integer,
    "type": fields.String,
    "target_id": fields.Integer,
    "task": fields.String,
    "modification": fields.String,
    "status": fields.String,
    "message": fields.String,
    "created_at": fields.DateTime(dt_format="iso8601"),
    "modified_at": fields.DateTime(dt_format="iso8601"),
}


# Create a resource to handle the API endpoint
class ApprovalResource(Resource):
    @jwt_required()
    @marshal_with(approval_fields)
    def get(self):
        current_user = get_jwt_identity()
        print("current_user", current_user)
        if current_user == 1:
            print("Admin User")
            approvals = Approvals.query.filter_by(status="NEW").all()
            return approvals
        else:
            return {"message": "Authorization error. Admin access required."}, 403

    @jwt_required()
    def put(self, approval_id):
        current_user = get_jwt_identity()
        print("current_user", current_user)
        if current_user == 1:
            print("Admin User")
            parser = reqparse.RequestParser()
            parser.add_argument(
                "status", type=str, required=True, help="Status must be provided"
            )

            args = parser.parse_args()
            new_status = args["status"]

            approval = Approvals.query.get(approval_id)

            if not approval:
                return {"message": "Approval not found"}, 404
            print(new_status.upper())
            if new_status.upper() not in ["APPROVED", "REJECTED"]:
                return {"message": "Invalid status. Use APPROVED or REJECTED"}, 400
            if new_status == "APPROVED":
                ApprovalsService.handleApprovedRequest(approval_id)
            approval.status = new_status.upper()
            db.session.commit()

            return {
                "message": f"Status updated to {new_status.upper()} for approval {approval_id}"
            }
        else:
            return {"message": "Authorization error. Admin access required."}, 403
