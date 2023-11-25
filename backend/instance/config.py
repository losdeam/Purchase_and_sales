
DIALECT = ''  # 要用的什么数据库
DRIVER = ''  # 连接数据库驱动
USERNAME = ''  # 用户名
PASSWORD = ''  # 密码
HOST = ''  # 服务器
PORT = ''  # 端口
DATABASE = ''  # 数据库名
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)



USERNAME = ''  # 用户名
PASSWORD = ''  # 密码
HOST = ''  # 服务器
PORT = ''  # 端口
DATABASE = ''  # 数据库名
REDIS_URL = "redis://{}:{}@{}:{}/{}".format(USERNAME, PASSWORD, HOST, PORT, DATABASE)





# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = ""
#授权码
MAIL_PASSWORD = ""
MAIL_DEFAULT_SENDER = ""