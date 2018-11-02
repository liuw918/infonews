from flask import current_app, render_template, request, jsonify, g
from info.constants import HOME_PAGE_MAX_NEWS
from info.models import News, Category
from info.modules.home import home_blu
from info.utils.common import user_login_data
from info.utils.response_code import RET, error_map


# 2.使用蓝图注册路由
@home_blu.route('/')
def index():

    user_login_data()

    # 按照点击量查询前十条新闻数据
    news_list =[]
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(10).all()
    except BaseException as e:
        current_app.aogger.error(e)

    news_list = [news.to_dict() for news in news_list]

    # 查询所有的分类数据，后端模板渲染
    categories = []
    try:
        categories = Category.query.all()
    except BaseException as e:
        current_app.logger.error(e)

    # 将模型转化为字典
    user =g.user.to_dict() if g.user else None

    return render_template("index.html",user=user, news_list=news_list, categories=categories)


@home_blu.route('/favicon.ico')
def favicon():
    # 网站小图标的请求是由浏览器自动请求，只需要实现路由即可
    # flask　中内置看返回静态文件的语法
    return current_app.send_static_file("news/favicon.ico")


# 获取新闻列表
@home_blu.route('/get_news_list')
def get_news_list():
    # 获取参数
    cid = request.args.get("cid")
    cur_page = request.args.get("cur_page")
    per_cunt = request.args.get("per_count", HOME_PAGE_MAX_NEWS)
    # 校验参数
    if not all([cid, cur_page, per_cunt]):
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])

    # 格式转换
    try:
        cid = int(cid)
        cur_page = int(cur_page)
        per_cunt = int(per_cunt)
    except BaseException as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])

    filter_list= []
    if cid != 1:  # 不是"最新"
        filter_list.append(News.category_id == cid)

    # 根据参数查询目标新闻　　按照发布时间和分类和页码查询新闻数据
    try:
        pn = News.query.filter(*filter_list).order_by(News.create_time.desc()).paginate(cur_page,per_cunt)
        news_list = [news.to_dict() for news in pn.items]
        total_page = pn.pages

    except BaseException as e:
        current_app.loggerr.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])

    data = {
        "news_list":news_list,
        "total_page":total_page
    }

    # 将新闻封装到json返回
    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK], data=data)
