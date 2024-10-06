import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery_config import celery, make_celery
from celery.result import AsyncResult
from flask import Flask, jsonify, send_from_directory
from models import db, User, PurchaseOrder, Product, Manager, Category
from datetime import datetime, date
from sqlalchemy import extract
import io
import csv
import os
import time
from config import REPORT_FOLDER
from flask_jwt_extended import jwt_required, get_jwt_identity


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grocerystore.database.sqlite3"
app.config["result_backend"] = "redis://localhost:6379/0"
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
db.init_app(app)


# app.config.from_object("config")  # Replace "config" with your actual config module

# Use make_celery to create the Celery app
celery = make_celery(app)
print("celery.conf.beat_schedule", celery.conf.beat_schedule)
# print("celery.conf.beat_schedule_interval", celery.conf.beat_schedule_interval)


def calculate_total_orders(user_id):
    current_month = datetime.now().month
    current_year = datetime.now().year
    total_orders = (
        db.session.query(PurchaseOrder)
        .filter(
            PurchaseOrder.user_id == user_id,
            PurchaseOrder.status == "SUCCESS",
            extract("month", PurchaseOrder.created_at) == current_month,
            extract("year", PurchaseOrder.created_at) == current_year,
        )
        .count()
    )
    return total_orders


def calculate_total_expenditure(user_id):
    with app.app_context():
        orders = PurchaseOrder.query.filter_by(user_id=user_id, status="SUCCESS").all()
        current_month = datetime.now().month
        current_year = datetime.now().year
        orders = (
            db.session.query(PurchaseOrder)
            .filter(
                PurchaseOrder.user_id == user_id,
                PurchaseOrder.status == "SUCCESS",
                extract("month", PurchaseOrder.created_at) == current_month,
                extract("year", PurchaseOrder.created_at) == current_year,
            )
            .all()
        )
        total_expenditure = sum(order.total for order in orders)
        return total_expenditure


def generate_monthly_user_activity_report1():
    print("generate_monthly_user_activity_report started triggered")


@celery.task
def generate_monthly_user_activity_report():
    print("generate_monthly_user_activity_report started")
    with app.app_context():
        now = datetime.now()
        # Get the current month in the format "DECEMBER"
        current_month = now.strftime("%B").upper()
        # Get the current year in the format "2023"
        current_year = now.strftime("%Y")

        print("inside with app context")

        users = User.query.filter_by(role="BUYER").all()
        contact_email = "gurukrupa.grocery.store@gmail.com"
        for user in users:
            print("calculating for ", user.id)
            total_orders = calculate_total_orders(user.id)
            total_expenditure = calculate_total_expenditure(user.id)

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Monthly Activity Report</title>
            </head>
            <body>
                <p>Dear {user.username},</p>
                <p>We hope this email finds you well and enjoying the convenience of shopping with <a href="http://localhost:8080/" style="color: #4285f4; text-decoration: underline;">Gurukrupa Grocery Store</a> ! </p>
                <p>As a valued customer, we wanted to take a moment to provide you with a summary of your purchases for the month of <b>{current_month} {current_year}</b>.</p>
                <h3>Monthly Activity Report Summary ({current_month} {current_year})</h3>
                <ul>
                    <li>Total Orders: {total_orders}</li>
                    <li>Total Expenditure: Rs {total_expenditure}</li>
                </ul>
                <p>We appreciate your continued trust and loyalty to <b><a href="http://localhost:8080/" style="color: #4285f4; text-decoration: underline;">Gurukrupa Grocery Store</a></b>. 
                If you have any feedback or suggestions, feel free to share them with us. Your satisfaction is our top priority!</p>
                <p>As a token of appreciation, here's a [Discount Code/Exclusive Offer] for your next purchase: [CODE123]. 
                Use it during checkout to enjoy additional savings.</p>
                <p>Thank you for choosing <b><a href="http://localhost:8080/" style="color: #4285f4; text-decoration: underline;">Gurukrupa Grocery Store</a></b>. We look forward to serving you again in the future.<p>

                <p>Happy Shopping!</p>
                
                <p>Gurukrupa Grocery Store Team</p>
                <p>Contact Information:<a href="mailto:gurukrupa.grocery.store@gmail.com" style="color: #4285f4; text-decoration: underline;">{contact_email}</a></p>
            </body>
            </html>
            """
            subject = f"""Monthly Activity Report - {current_month} {current_year}"""
            sendEmail(subject, html_content, user.username)


@celery.task
def send_daily_visit_reminder():
    # users = User.query.filter_by(role="BUYER").all()
    today_date = date.today()
    inactive_buyer_users = User.query.filter(
        User.last_login < datetime(today_date.year, today_date.month, today_date.day),
        User.role == "BUYER",
    ).all()

    contact_email = "gurukrupa.grocery.store@gmail.com"
    for user in inactive_buyer_users:
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Don't Miss Out on Fresh Groceries Today!</title>
        </head>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">

        <div style="background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #333333;">Don't Miss Out on Fresh Groceries at <b>Gurukrupa Grocery Store</b> Today!</h2>
            <p>Dear {user.username},</p>
            <p>We hope this message finds you well. At Gurukrupa Grocery Store, we appreciate your continued support in choosing us for your grocery needs.</p>
            <p>We noticed that you haven't visited our online store today, and we wanted to remind you about 3 reasons to shop with us today:</p>
            <ul>
                <li><strong>Fresh and Quality Products:</strong> We source the finest quality products to ensure your satisfaction.</li>
                <li><strong>Convenient Online Shopping:</strong> Save time by shopping from the comfort of your home.</li>
                <li><strong>Exclusive Discounts:</strong> Check out our latest promotions to get the best deals on your favorite items.</li>
            </ul>
            <p>Visit our online store now: <a href="http://localhost:8080/" style="color: #4285f4; text-decoration: underline;">Gurukrupa Grocery Store</a></p>
            <p>Thank you for being a valued customer, and we look forward to serving you soon.</p>
            <p>Best regards,</p>
            <p>Gurukrupa Grocery Store</p>
            <p>Contact Information:<a href="mailto:gurukrupa.grocery.store@gmail.com" style="color: #4285f4; text-decoration: underline;">{contact_email}</a></p>
        </div>
                </div>

        </body>
        </html>
        """
        subject = "Daily Reminder : Don't Miss Out on Fresh Groceries Today!"
        sendEmail(subject, html_content, user.username)


def sendEmail(subject, html_content, to_email):
    # Rediff SMTP server and port
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # sender_email = "sameerinaik31@gmail.com"
    # password = "nafefoodepmrmguu"
    sender_email = "gurukrupa.grocery.store@gmail.com"
    password = "zgomwridedwapjcd"
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Attach HTML content
    message.attach(MIMEText(html_content, "html"))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Start TLS for security
            server.starttls()
            server.set_debuglevel(1)
            # Login to the Rediff email account
            server.login(sender_email, password)

            # Send the email
            server.sendmail(sender_email, to_email, message.as_string())

        print("Email sent successfully to ", to_email)
    except Exception as e:
        print(f"Error sending email: {e}")


@celery.task
def export_products_csv_async(manager_id):
    # Query products for manager_id from the database
    dbCategoryList = Category.query.filter(Category.owner == manager_id).all()
    dbCategoryIdList = []
    for category in dbCategoryList:
        dbCategoryIdList.append(category.id)
        print("dbCategoryIdList ", dbCategoryIdList)
        products = (
            Product.query.filter(Product.categoryid.in_(dbCategoryIdList))
            .order_by(Product.categoryid)
            .all()
        )

    # Prepare CSV data
    csv_data = io.StringIO()
    csv_writer = csv.writer(csv_data)

    # Write CSV header
    csv_writer.writerow(
        [
            "Product ID",
            "Name",
            "Category ID",
            "Sell Quantity",
            "Sell Unit",
            "Stock Quantity",
            "Stock Unit",
            "Price",
            "Discounted Price",
            "Available",
            "Manufacturing Date",
            "Expiry Date",
        ]
    )

    # Write product data to CSV
    for product in products:
        csv_writer.writerow(
            [
                product.id,
                product.name,
                product.categoryid,
                product.sell_quantity,
                product.sell_unit,
                product.stock_quantity,
                product.stock_unit,
                product.price,
                product.discounted_price,
                product.available,
                product.manufacturingdate,
                product.expirydate,
            ]
        )

    # Save the CSV file on the server
    print("app.root.path", app.root_path)
    full_path = os.path.join(app.root_path, REPORT_FOLDER)
    file_name = f'products_export_{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.csv'
    file_path = f"{full_path}/{file_name}"
    with open(file_path, "w") as file:
        file.write(csv_data.getvalue())

    time.sleep(7)
    return {"file_name": file_name, "status": "Task completed"}


def defineExportRoutes(app):
    @app.route("/product/export_products_csv")
    @jwt_required()
    def export_products_csv():
        # Trigger the Celery task asynchronously
        current_user = get_jwt_identity()
        manager = Manager.query.filter(Manager.userid == current_user).first()
        if manager:
            task = export_products_csv_async.apply_async(args=(manager.id,))
            return jsonify({"job_id": task.id})

    @app.route("/product/export_status/<job_id>")
    def export_status(job_id):
        task = AsyncResult(job_id, app=celery)

        if task.ready():
            # Task is complete, return the CSV file
            result = task.result
            filename = result.get("file_name")
            print("#####result.file_url", filename)
            full_path = os.path.join(app.root_path, REPORT_FOLDER)
            return send_from_directory(
                full_path,
                filename,
                as_attachment=True,
                mimetype="text/csv",
                download_name="exported_file.csv",
            )
        else:
            # Task is still running or hasn't started
            return f"Export task is in progress. Status: {task.status}"
