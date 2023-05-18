from flask import Flask
from Application.database import db
from flask_cors import CORS
from Application.worker import *
from os import path
api=None
app=None
def create_app():
    app=Flask(__name__)
    CORS(app)
    cd= path.abspath(path.dirname('Bloglite'))
    print(cd)

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+path.join(cd,"bloglite.sqlite3")
    app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///bloglite.sqlite3'
    app.config["DEBUG"]=False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
    app.config['SECRET_KEY'] = 'abcd'
    db.init_app(app)
    return app

app=create_app()
#api=create_app()
app.app_context().push()

from Application.api import Register

from Application.models import *

#from Application.controllers import *



celery=celery
CELERY_BROKER_URL="redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/2"

celery.conf.update(
    broker_url="redis://127.0.0.1:6379/1",
    result_backend="redis://127.0.0.1:6379/2",
    timezone="Asia/Kolkata"
)

celery.Task = ContextTask


if __name__=="__main__":
    db.create_all()
    app.run(debug = True)