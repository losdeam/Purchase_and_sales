from flask import Flask
# 跨域
from flask_cors import CORS
# RESTful API
from flask_restx import Api
# 导入需要初始化的组件
from .extensions import db , mail, login_manager,redis_client

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
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    redis_client.init_app(app)
    # 导入并注册命名空间
    from . import auth,goods
    from . import database
    
    api.add_namespace(database.api)
    api.add_namespace(auth.api)
    api.add_namespace(goods.api)

    return app
