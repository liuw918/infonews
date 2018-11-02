from flask import session, current_app, g
from info.models import User, News


# 过滤器的本质：函数
# 1.必须设置参数接收的模板变量
# 2.将转换后的结果返回


def func_index_convert(index):
    index_dict = {1: "first", 2: "second", 3: "third"}
    return index_dict.get(index, "")


# 获取用户登陆信息
def user_login_data():
    # 在根路由中判断用户是否登陆
    user_id = session.get("user_id")

    user = None
    if user_id:
        # 查询用户信息
        try:
            user = User.query.get(user_id)
        except BaseException as e:
            current_app.logger.error(e)

    g.user = user
