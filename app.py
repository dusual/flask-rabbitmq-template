from flask import Flask
from celery import Celery

from api import urls_api

app = Flask(__name__)
app.register_blueprint(urls_api)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)








