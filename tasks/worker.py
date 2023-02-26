from flask import Flask
from celery import Celery
from os.path import exists
import csv


app = Flask(__name__)
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app.config.update(
    CELERY_BROKER_URL='amqp://admin:password@broker-rabbitmq:5672/demo',
    CELERY_RESULT_BACKEND='rpc://admin:password@broker-rabbitmq:5672/demo'
)

celery = make_celery(app)

@celery.task
def aggregator(payload):
    with (open('./csv_file.csv', 'a')) as f:
        writer = csv.writer(f)
        for pred in payload['data']['preds']:
            writer.writerow([pred['image_frame'], pred['prob'], ' '.join(pred['tags'])])
    return "OK"