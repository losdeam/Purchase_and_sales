from flask import Flask
# 跨域
from flask_cors import CORS
# RESTful API
from flask_restx import Api
# 导入需要初始化的组件
from .extensions import db , redis_client,login_manager,mongo ,socketio

def create_app():
    # 创造并配置app, instance_relative_config=True表示配置文件是相对于instance folder的相对路径
    app = Flask(__name__, instance_relative_config=True)

    # RESTful API
    api = Api(app, version='1.0', title='purchase_sale  API',
              description='进销货系统接口文档', prefix='/api')

    # 跨域
    CORS(app, supports_credentials=True)

    # 从 config.py 文件中读取配置
    app.config.from_pyfile('config.py')

    # 初始化各种组件
    login_manager.init_app(app)
    db.init_app(app)
    redis_client.init_app(app)
    mongo.init_app(app)
    socketio.init_app(app,cors_allowed_origins="*")

    # 导入并注册命名空间
    from . import goods
    from . import database
    from . import auth
    from . import recognition
    api.add_namespace(database.api)
    api.add_namespace(goods.api)
    api.add_namespace(auth.api)
    api.add_namespace(recognition.api)
    return app
