from app import app
from celery import Celery

CELERY_BROKER_URL = 'pyamqp://admin:password:rabbit_password@broker-rabbitmq:5672//'
CELERY_RESULT_BACKEND = 'rpc://admin:password@broker-rabbitmq:5672//'

celery = Celery(app.name, broker=CELERY_BROKER_URL)
celery.conf.update(app.config)