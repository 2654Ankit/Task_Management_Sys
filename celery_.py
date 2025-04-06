from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv
load_dotenv()



app = Celery(
    'celery_app',
    broker=os.getenv('BROKER_URL','redis://localhost:6379/0'),
    backend=os.getenv('BACKEND_URL','redis://localhost:6379/1'),
)

app.autodiscover_tasks(['celery_app.tasks.task'])

# Timezone configuration for India
app.conf.timezone = 'Asia/Kolkata'
app.conf.enable_utc = False

# Scheduled tasks configuration
app.conf.beat_schedule = {
    'transfer-tasks-daily': {
        'task': 'celery_app.tasks.task.transfer_active_tasks',
        'schedule': crontab(hour=22, minute=45),  # 9:39 PM IST
    },
}