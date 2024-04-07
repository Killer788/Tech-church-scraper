import os

from celery import Celery
from django.conf import settings


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tech_church_scraper_with_django.settings')

app = Celery('tech_church_scraper_with_django', broker=settings.CELERY_BROKER_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'every_60_seconds_scrape_remaining_articles': {
        'task': 'techchurch.tasks.scrape_remaining_articles',
        'schedule': 60,
    },
}

# Load task modules from all registered Django apps
app.autodiscover_tasks()

# celery -A tech_church_scraper_with_django worker -l INFO -P eventlet
# celery -A tech_church_scraper_with_django beat --loglevel=INFO
