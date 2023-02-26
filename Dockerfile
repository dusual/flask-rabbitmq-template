FROM python:3.9

RUN pip install pipenv
ADD . /app
WORKDIR /app
RUN pip install flask
RUN pip install celery
RUN pip install watchdog
RUN pip install gunicorn[gevent]

EXPOSE 8000
CMD python app.py