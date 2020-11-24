import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from src.event_dispatcher import EventDispatcher

app = Flask(__name__)
CORS(app)

db_pg = False

if db_pg:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/bac_rest"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'max_overflow': 20
    }
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db?timeout=60')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # for print the sql query

db = SQLAlchemy(app)
from src import routes  # importing for creating all the schema on un-existing case
from src.models.point.model_point_store_history import PointStoreHistoryModel  # this one doesn't exist on routes

db.create_all()

with app.app_context():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        from src.background import Background

        Background.run()
