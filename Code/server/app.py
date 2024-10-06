from flask import Flask, session

from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user

"""from database import database"""
from models import db
from authentication import defineAuthenticationRoutes
from views import defineRoutes
from viewsDashboard import defineDashboardRoutes
from summary import defineSummaryRoutes
from search import defineSearchRoutes
from error import defineErrorRoutes
from api.api import defineAPIRoutes
from celery_jobs import defineExportRoutes
from cache_utils import init_cache

cache_config = {"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 300}
app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = "Gurukrupa"
print("My name is : ", __name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grocerystore.database.sqlite3"
db.init_app(app)

init_cache(app, config=cache_config)

app.app_context().push()

defineErrorRoutes(app)
defineAuthenticationRoutes(app)
defineRoutes(app)
defineDashboardRoutes(app)
defineSummaryRoutes(app)
defineSearchRoutes(app)
defineAPIRoutes(app)
defineExportRoutes(app)
# create a route accept {id}. Route will be called. task.py->exportProductDetailsAsCSV.
# Send storemanager id.

# Load Celery configuration from celery_config.py
###app.config.from_object("celery_config")
# Create Celery instance
###celery = celery
###celery.conf.update(app.config)

if __name__ == "__main__":
    app.run(debug=True, port=7000)
