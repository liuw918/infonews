from flask import current_app, render_template, abort, g
from info.models import News
from info.modules.news import news_blu
from info.utils.common import user_login_data


# 新闻详情
@news_blu.route('/<int:news_id>')  # 路由变量来接收新闻id
def news_detail(news_id):
    # 根据新闻id查询该新闻数据
    try:
        news = News.query.get(news_id)
    except BaseException as e:
        current_app.logger.error(e)
        abort(500)

    # 按照点击量查询前十条新闻数据
    news_list =[]
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(10).all()
    except BaseException as e:
        current_app.aogger.error(e)

    news_list = [news.to_dict() for news in news_list]

    # 点击量加１
    news.clicks += 1

    # 在根路由中判断用户是否登陆
    user_login_data()

    # 将模型转化为字典
    user = g.user.to_dict() if g.user else None

    # 将数据传入模板渲染
    return render_template("detail.html", news=news.to_dict(), news_list=news_list, user=user)