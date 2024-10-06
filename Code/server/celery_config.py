from celery import Celery
from celery.schedules import crontab


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["result_backend"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    # celery.conf.update(app.config)
    celery.conf.timezone = "Asia/Kolkata"

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    celery.conf.beat_schedule = {
        "generate-monthly-activity-report": {
            "task": "celery_jobs.generate_monthly_user_activity_report",
            #"schedule": 120,
            "schedule": crontab(minute=45, hour=12,day_of_month=28)
        },
        "send-daily-reminder": {
            "task":"celery_jobs.send_daily_visit_reminder",
            #"schedule": 120,
            "schedule": crontab(minute=45, hour=12),
        },
    }
    celery.conf.beat_schedule_interval = 60
    return celery


def define_celery():
    celery_instance = Celery(
        __name__, backend="redis://localhost:6379/0", broker="redis://localhost:6379/0"
    )

    # Additional configuration for celery_instance if needed

    return celery_instance


# Define the celery app
celery = define_celery()

# Demo
"""celery.conf.beat_schedule = {
    "generate-monthly-report": {
        "task": "celery_jobs.generate_monthly_user_activity_report",
        "schedule": 30,
    },
}"""
