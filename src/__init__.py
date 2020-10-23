import os
from threading import Thread

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from src.modbus.services.point_store_cleaner import PointStoreCleaner

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # for print the sql query

db = SQLAlchemy(app)
from src import routes

if not not os.environ.get("WERKZEUG_RUN_MAIN"):
    from src.modbus.models.point_store import ModbusPointStoreModel

    db.create_all()
    from src.bacnet.services.network import Network
    from src.modbus.services.tcp_registry import TcpRegistry
    from src.modbus.services.tcp_polling import TcpPolling
    from src.modbus.services.rtu_polling import RtuPolling
    from src.modbus.services.rtu_registry import RtuRegistry

    Network.get_instance().start()

    TcpRegistry.get_instance().register()
    tcp_polling_thread = Thread(target=TcpPolling.get_instance().polling)
    tcp_polling_thread.start()

    RtuRegistry.get_instance().register()
    rtu_polling_thread = Thread(target=RtuPolling.get_instance().polling)
    rtu_polling_thread.start()

    point_cleaner_thread = Thread(target=PointStoreCleaner.register)
    point_cleaner_thread.start()
