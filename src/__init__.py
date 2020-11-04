import os
from threading import Thread

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# from src.modbus.services.point_store_cleaner import PointStoreCleaner
from src.services.histories.point_store_history_cleaner import PointStoreHistoryCleaner

app = Flask(__name__)
CORS(app)

# TMP CONFIGS
db_pg = False
enable_tcp = True
enable_rtu = True
enable_cleaner = True

if db_pg:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/bac_rest"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'max_overflow': 20
    }
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # for print the sql query

db = SQLAlchemy(app)
from src import routes

if not not os.environ.get("WERKZEUG_RUN_MAIN"):
    from src.models.point.model_point_store_history import PointStoreHistoryModel  # for to create this model

    db.create_all()
    # from src.source_drivers.bacnet.services.network import Network
    from src.source_drivers.modbus.services.tcp_registry import TcpRegistry
    from src.source_drivers.modbus.services.tcp_polling import TcpPolling
    from src.source_drivers.modbus.services.rtu_polling import RtuPolling
    from src.source_drivers.modbus.services.rtu_registry import RtuRegistry
    from src.services.histories.history_interval import HistoryInterval

    # Network.get_instance().start()

    if enable_tcp:
        TcpRegistry.get_instance().register()
        tcp_polling_thread = Thread(target=TcpPolling.get_instance().polling)
        tcp_polling_thread.start()

    if enable_rtu:
        RtuRegistry.get_instance().register()
        rtu_polling_thread = Thread(target=RtuPolling.get_instance().polling)
        rtu_polling_thread.start()

    history_thread = Thread(target=HistoryInterval.get_instance().sync_interval)
    history_thread.start()

    if enable_cleaner:
        point_cleaner_thread = Thread(target=PointStoreHistoryCleaner.register)
        point_cleaner_thread.start()
