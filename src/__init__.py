import os
from threading import Thread

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # for print the sql query

db = SQLAlchemy(app)
from src import routes

if not not os.environ.get("WERKZEUG_RUN_MAIN"):
    db.create_all()
    # from src.sourceDrivers.bacnet.services.network import Network
    from src.sourceDrivers.modbusCopy.services.tcp_registry import TcpRegistry
    from src.sourceDrivers.modbusCopy.services.tcp_polling import TcpPolling

    # Network.get_instance().start()

    # TcpRegistry.get_instance().register()
    # tcp_polling_thread = Thread(target=TcpPolling.get_instance().polling)
    # tcp_polling_thread.start()
