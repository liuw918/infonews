import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from config import ProductConfig, Config

# 将数据库连接对象全句化
db = None  # type: SQLAlchemy
sr = None  # type: StrictRedis

# 日志配置（将日志文件保存到文件中）
def setup_log():
    # 设置日志的记录等级
    logging.basicConfig(level=logging.DEBUG) # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 定义函数　　封装应用的创建和配置　工厂函数（调用者提货提供生产物料，函数内部封装创建过程）
def create_app(config_type):
    app = Flask(__name__)
    # 从对象加载配置信息
    app.config.from_object(ProductConfig)

    # 从对象加载配置信息
    app.config.from_object(Config)

    # 声明全局变量
    global db, sr

    # 创建数据库连接对象
    db = SQLAlchemy(app)
    # 创建redis连接对象
    sr = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT,decode_responses=True)

    # 初始化session对象
    Session(app)

    # 初始化迁移器
    Migrate(app, db)

    from info.modules.home import home_blu
    # 3.注册蓝图
    app.register_blueprint(home_blu)

    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    # 配置日志
    setup_log()

    # import* 语法在函数/方法里不受支持
    # from info.modules import *
    import info.models

    return app