from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import enum

db = SQLAlchemy()

# Create your models here.


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String)
    registered_at = db.Column(db.DateTime(), default=datetime.now)
    last_login = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    def __init__(self, firstname, lastname, username, password, role):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = generate_password_hash(password, method="sha256")
        self.role = role

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")

        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(
            id=self.id,
            username=self.username,
            password=self.password,
            firstname=self.firstname,
            lastname=self.lastname,
            role=self.role,
        )


"""class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100))
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100))
    registered_at = db.Column(db.DateTime(), default=datetime.now)
    last_login = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)"""


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(
        db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False
    )
    approved = db.Column(db.Integer, default=0)  # 0 Not Approved, 1 Approved
    registered_at = db.Column(db.DateTime(), default=datetime.now)
    last_login = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    owner = db.Column(db.Integer, db.ForeignKey("manager.id"))
    created_at = db.Column(db.DateTime(), default=datetime.now)
    modified_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    deleted = db.Column(db.Integer, default=0)  # 0 Not Deleted, 1 Deleted
    # One to Many relationship between Category and Product
    products = db.relationship("Product", backref="category")

    def to_dict(self):
        return dict(id=self.id, name=self.name, owner=self.owner)


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    imagename = db.Column(db.String(50))
    description = db.Column(db.String(500))
    categoryid = db.Column(db.Integer, db.ForeignKey("category.id"))
    sell_quantity = db.Column(
        db.Integer
    )  # 500g or 250g => Here 500 is sellQuantity, g is sellUnit
    sell_unit = db.Column(db.String)
    stock_quantity = db.Column(db.Integer)
    stock_unit = db.Column(db.String)
    price = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    discounted_price = db.column_property(price * (100 - discount) / 100)
    available = db.Column(db.Integer)  # 0 Unavailable, 1 Available
    manufacturingdate = db.Column(db.Date())
    expirydate = db.Column(db.Date())
    created_at = db.Column(db.DateTime(), default=datetime.now)
    modified_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    deleted = db.Column(db.Integer, default=0)  # 0 Not Deleted, 1 Deleted

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "imagename": self.imagename,
            "description": self.description,
            "categoryid": self.categoryid,
            "sell_quantity": self.sell_quantity,
            "sell_unit": self.sell_unit,
            "stock_quantity": self.stock_quantity,
            "stock_unit": self.stock_unit,
            "price": self.price,
            "discount": self.discount,
            "discounted_price": self.discounted_price,
            "available": self.available,
            "manufacturingdate": str(self.manufacturingdate),  # Convert date to string
            "expirydate": str(self.expirydate),  # Convert date to string
            "created_at": str(self.created_at),  # Convert datetime to string
            "modified_at": str(self.modified_at),  # Convert datetime to string
        }


class Address(db.Model):
    _tablename_ = "address"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    contact_person_name = db.Column(db.String(100), nullable=False)
    contact_person_number = db.Column(db.Integer)
    housename = db.Column(db.String(100), nullable=False)
    line_address = db.Column(db.String(100), nullable=False)
    town_city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Integer, db.ForeignKey("state.id"))
    landmark = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.Integer)
    defaultAddress = db.Column(db.Integer)  # 0=false, 1=true


class State(db.Model):
    _tablename_ = "state"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    total = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    modified_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    status = db.Column(db.Integer)
    apply_promo_code = db.Column(db.Integer, default=0)
    db.UniqueConstraint(id, user_id)


class CartItem(db.Model):
    __tablename__ = "cart_item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.Integer, db.ForeignKey("cart.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    discounted_price = db.column_property(price * (100 - discount) / 100)
    status = db.Column(db.Integer)  # 0-Out of Stock, 1-Available
    created_at = db.Column(db.DateTime(), default=datetime.now)
    modified_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    db.UniqueConstraint(session_id, product_id)


# class PurchaseOrderStatus(db.Model):
#    __tablename__='purchase_order_status'
#    id= db.Column(db.Integer, primary_key = True, autoincrement = True)
#    status= db.Column(db.String(50), nullable = False)


class PurchaseOrderStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    PAYMENTFAILED = "PAYMENT FAILED"


class PurchaseOrder(db.Model):
    __tablename__ = "purchase_order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    session_id = db.Column(db.Integer, db.ForeignKey("cart.id"))
    shipping_charges = db.Column(db.Integer)
    total = db.Column(db.Integer)
    status = db.Column(
        db.Enum(PurchaseOrderStatus, values_callable=lambda obj: [e.value for e in obj])
    )  # 0-Failed, 1-Success
    promo_code = db.Column(db.String)
    delivery_address = db.Column(db.Integer, db.ForeignKey("address.id"))
    delivery_date_estimated = db.Column(
        db.DateTime(), default=datetime.now() + timedelta(days=1)
    )
    delivery_date_actual = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), default=datetime.now)
    modified_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    db.UniqueConstraint(id, user_id)


class PurchaseOrderItem(db.Model):
    __tablename__ = "purchase_order_item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey("purchase_order.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    discounted_price = db.column_property(price * (100 - discount) / 100)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    modified_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    db.UniqueConstraint(order_id, product_id)


class PaymentDetails(db.Model):
    _tablename_ = "payment_details"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("purchase_order.id"))
    payment_mode = db.Column(db.Integer, db.ForeignKey("payment_mode.id"))
    information = db.Column(db.String)  # message returned by payment gateway
    status = db.Column(db.Integer)  # 0-Failed, 1-Success
    created_at = db.Column(db.DateTime(), default=datetime.now)
    modified_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)


class PaymentMode(db.Model):
    _tablename_ = "payment_mode"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mode = db.Column(db.String, unique=True)


class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    message = db.Column(db.String, nullable=False)
    severity = db.Column(db.String)
    owner = db.Column(db.Integer, db.ForeignKey("manager.id"))


class Approvals(db.Model):
    _tablename_ = "approvals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requester_id = db.Column(db.Integer, db.ForeignKey("manager.id"))
    type = db.Column(db.String)  # CATEGORY,MANAGER
    target_id = db.Column(db.Integer)  # id of record to be modified. Used for Category (EDIT,DELETE) and MANAGER(CREATE)
    task = db.Column(db.String)  # CREATE,EDIT,DELETE
    modification = db.Column(db.String)  # Used in case of CREATE,EDIT
    status = db.Column(db.String)  # NEW,APPROVED,REJECTED
    message = db.Column(db.String)  # Message for Admin
    created_at = db.Column(db.DateTime(), default=datetime.now)
    modified_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return dict(id=self.id,requester_id=self.requester_id,type=self.type,target_id=self.target_id,task=self.task,modification=self.modification,message=self.message,status=self.status)
        
