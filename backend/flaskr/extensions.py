# 导入各种拓展
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis


# 实例化
db = SQLAlchemy()
redis_client = FlaskRedis()
