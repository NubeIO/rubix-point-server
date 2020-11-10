import os
from threading import Thread

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from src.event_dispatcher import EventDispatcher

app = Flask(__name__)
CORS(app)

# TMP CONFIGS
db_pg = False
enable_histories = True
enable_tcp = False
enable_rtu = True
enable_cleaner = True

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

# Other Services
from src.services.histories.history_local import HistoryLocal
from src.services.histories.point_store_history_cleaner import PointStoreHistoryCleaner
# Source Drivers
# from src.source_drivers.bacnet.services.network import Network
from src.source_drivers.modbus.services.tcp_registry import TcpRegistry
from src.source_drivers.modbus.services.tcp_polling import TcpPolling
from src.source_drivers.modbus.services.rtu_polling import RtuPolling
from src.source_drivers.modbus.services.rtu_registry import RtuRegistry

from src import routes

db.create_all()

if not not os.environ.get("WERKZEUG_RUN_MAIN"):

    if enable_histories:
        histories_thread = Thread(target=HistoryLocal.get_instance().sync_interval)
        histories_thread.start()

    # Network.get_instance().start()

    if enable_tcp:
        TcpRegistry.get_instance().register()
        tcp_polling_thread = Thread(target=TcpPolling.get_instance().polling)
        tcp_polling_thread.start()

    if enable_rtu:
        RtuRegistry.get_instance().register()
        rtu_polling_thread = Thread(target=RtuPolling.get_instance().polling)
        rtu_polling_thread.start()

    if enable_cleaner:
        point_cleaner_thread = Thread(target=PointStoreHistoryCleaner.register)
        point_cleaner_thread.start()
