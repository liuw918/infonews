from flask import Blueprint


# 1.创建蓝图
passport_blu = Blueprint("passport", __name__, url_prefix="/passport")

# 4.关联试图2函数（避免循环导入）
from .views import *