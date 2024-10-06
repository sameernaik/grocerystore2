cd "$(dirname "$0")"
current_directory=$(pwd)
echo "Current directory is: $current_directory"
cd server
rm -rf celerybeat-schedule.db
celery -A celery_jobs.celery beat --loglevel=info --max-interval=60