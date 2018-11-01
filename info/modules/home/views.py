import logging
from flask import current_app, render_template, session

from info.models import User, News
from info.modules.home import home_blu


# 2.使用蓝图注册路由
@home_blu.route('/')
def index():
    # 在根路由中判断用户是否登陆
    user_id = session.get("user_id")

    user = None
    if user_id:
        # 查询用户信息
        try:
            user = User.query.get(user_id)
        except BaseException as e:
            current_app.logger.error(e)

    # news_list =[]
    # try:
    #     news_list = News.query.order_by(News.clicks.desc()).limit(10).all()
    # except BaseException as e:
    #     current_app.aogger.error(e)
    #
    # news_list = [News.to_dict() for News in news_list]

    # 将模型转化为字典
    user =user.to_dict() if user else None

    return render_template("index.html",user=user)


@home_blu.route('/favicon.ico')
def favicon():
    # 网站小图标的请求是由浏览器自动请求，只需要实现路由即可
    # flask　中内置看返回静态文件的语法
    return current_app.send_static_file("news/favicon.ico")