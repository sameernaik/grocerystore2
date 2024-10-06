cd "$(dirname "$0")"
current_directory=$(pwd)
echo "Current directory is: $current_directory"
cd server
celery -A celery_jobs.celery worker --loglevel=info -E