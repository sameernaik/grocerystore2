from datetime import datetime
from sqlalchemy.exc import IntegrityError
from models import db, Approvals, Category, Product, Manager


class ApprovalsService:
    @staticmethod
    def create_approval(
        requester_id, approval_type, target_id, task, modification, status,message
    ):
        try:
            approval = Approvals(
                requester_id=requester_id,
                type=approval_type,
                target_id=target_id,
                task=task,
                modification=modification,
                status=status,
                created_at=datetime.now(),
                modified_at=datetime.now(),
                message=message
            )
            db.session.add(approval)
            db.session.commit()
            return approval
        except IntegrityError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_approval(approval_id):
        return Approvals.query.get(approval_id)

    @staticmethod
    def update_approval(approval_id, status):
        approval = Approvals.query.get(approval_id)
        if approval:
            approval.status = status
            approval.modified_at = datetime.now()
            db.session.commit()
            return approval
        return None

    @staticmethod
    def delete_approval(approval_id):
        approval = Approvals.query.get(approval_id)
        if approval:
            db.session.delete(approval)
            db.session.commit()
            return approval
        return None

    @staticmethod
    def handle_category_create(approval):
        print("Category Create")
        try:
            category_name = approval.modification
            category_owner = approval.requester_id
            dbcategory = Category.query.filter(
                Category.name == approval.modification
            ).first()
            if dbcategory:
                return print("category_code already exists", dbcategory)
            else:
                new_category = Category(name=category_name, owner=category_owner)
                db.session.add(new_category)
                db.session.commit()
                print("Category created successfully", category_name, category_owner)
                return
        except Exception as e:
            print("Internal Server Error ", e)

    @staticmethod
    def handle_category_edit(approval):
        print("Category Edit")
        try:
            id = approval.target_id
            dbcategory = Category.query.filter(Category.id == id).first()
            if dbcategory:
                dbcategory.name = approval.modification
                db.session.add(dbcategory)
                db.session.commit()
                return dbcategory, 200
            else:
                print("category not found")
        except NotFoundException:
            print("NotFoundError")
        except Exception as e:
            print("Internal Server Error ", e)
        return

    @staticmethod
    def handle_category_delete(approval):
        try:
            id = approval.target_id
            print("Deleting Category ", id)
            dbcategory = Category.query.filter(Category.id == id).first()
            print("dbcategory ", dbcategory, id)
            if dbcategory is None:
                print("category not found")
            else:
                Product.query.filter(Product.categoryid == id).delete()
                Category.query.filter(Category.id == id).delete()
                db.session.commit()
                print("Deleted Category ", id)
        except NotFoundException:
            raise
        except Exception as e:
            raise InternalServerError(str(e))
        return

    @staticmethod
    def handle_user_edit(approval):
        try:
            manager_id = approval.requester_id
            print("Handling StoreManager addition request for manager id ", manager_id)
            dbmanager = Manager.query.filter(Manager.id == manager_id).first()
            if dbmanager:
                dbmanager.approved = approval.modification
                db.session.add(dbmanager)
                db.session.commit()
                print("User Edit")
                return dbmanager, 200
            else:
                print("Approval Error: Manager not found for manager id", manager_id)
        except NotFoundException:
            print("NotFoundError")
        except Exception as e:
            print("Internal Server Error ", e)

    @staticmethod
    def handleApprovedRequest(approval_id):
        print("Handling approval for ", approval_id)
        approval = ApprovalsService.get_approval(approval_id)
        print(approval.to_dict())
        if approval.type == "CATEGORY":
            print("Handling Category request")
            task = approval.task
            if task == "CREATE":
                ApprovalsService.handle_category_create(approval)
            elif task == "EDIT":
                ApprovalsService.handle_category_edit(approval)
            elif task == "DELETE":
                ApprovalsService.handle_category_delete(approval)
            else:
                print(f"Unknown task: {task}")
        elif approval.type == "STORE_MANAGER":
            print("Handling User approval request")
            task = approval.task
            if task == "EDIT":
                ApprovalsService.handle_user_edit(approval)
