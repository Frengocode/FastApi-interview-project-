# celery_app.py
from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    'app',
    broker='sqla+sqlite:///./db.sqlite3', 
    backend='db+sqlite:///./db.sqlite3' 
)

celery_app.conf.update(
    task_routes={
        'app.tasks.*': {'queue': 'default'}
    },
    beat_schedule={
        'delete-old-books-every-day': {
            'task': 'tasks.delete_old_books',
            'schedule': crontab(hour=0, minute=0),  
        },
    }
)
