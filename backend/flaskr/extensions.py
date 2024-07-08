# 导入各种拓展
# from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from collections import defaultdict
# 实例化
# db = SQLAlchemy()
mongo = PyMongo()
redis_client = FlaskRedis()
login_manager = LoginManager()
socketio = SocketIO()

logging = defaultdict(list)
train_queue = []
running_process= []

