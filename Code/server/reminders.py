import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import User, Order
import time

app = Flask(__name__)

db = SQLAlchemy(app)

sender_email = "abc@gmail.com"

smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "abc@gmail.com"
smtp_password = "1234567"

# Demo : Adjust the time for 2 mins from now to demo mail being sent.
reminder_time = datetime.now().replace(hour=19, minute=19, second=0, microsecond=0)


def send_reminder(user):
    subject = "Daily Reminder"
    message = f"Hello {user.name}! It seems like you haven't visited or bought anything today. Please consider checking out our products on GrocerEase."

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = user.email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, user.email, msg.as_string())
        print(f"Reminder email sent to {user.email} successfully!")
    except Exception as e:
        print(f"Failed to send reminder email to {user.email}: {e}")


def check_user_activity(user):
    today = datetime.today().date()
    user_orders_today = (
        Order.query.filter_by(user_id=user.id).filter(Order.buy_at >= today).all()
    )

    return not user_orders_today


if __name__ == "__main__":
    while True:
        current_time = datetime.now()
        time_until_reminder = reminder_time - current_time

        if time_until_reminder.total_seconds() < 0:
            time_until_reminder += timedelta(days=1)

        print(
            f"Waiting for {time_until_reminder.seconds} seconds until the reminder time..."
        )
        time.sleep(time_until_reminder.seconds)

        all_users = User.query.filter_by(role="user").all()
        for user in all_users:
            if check_user_activity(user):
                send_reminder(user)
            else:
                print(
                    f"{user.name} has visited or bought something today. No reminder needed."
                )
