from celery import Celery
from celery.schedules import crontab
from extensions import get_redis

# Initialize Celery application
app = Celery(
    'celery_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    # include=['celery_app.tasks.task']  # Explicit task imports
)
app.autodiscover_tasks(['celery_app.tasks.task'])

# Timezone configuration for India
app.conf.timezone = 'Asia/Kolkata'
app.conf.enable_utc = False

# Scheduled tasks configuration
app.conf.beat_schedule = {
    'transfer-tasks-daily': {
        'task': 'celery_app.tasks.task.transfer_active_tasks',
        'schedule': crontab(hour=17, minute=45),  # 9:39 PM IST
    },
}

