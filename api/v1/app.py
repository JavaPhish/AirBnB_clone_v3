#!/usr/bin/python3
"""Creating a flask app
"""
from models import storage
from flask import Flask
from api.v1.views.index import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_db(self):
    storage.close()


if __name__ == '__main__':
    if getenv('HBNB_API_HOST') and getenv('HBNB_API_PORT'):
        app.run(
               host=getenv('HBNB_API_HOST'),
               port=getenv('HBNB_API_PORT'),
               debug=True)
    else:
        app.run(
               host='0.0.0.0',
               port='5000',
               debug=True)
