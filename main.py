from flask import session
from flask_migrate import MigrateCommand
from flask_script import Manager
from info import create_app


# 创建应用
app = create_app("pro")


# 创建管理器
mgr = Manager(app)

# 管理器生成迁移命令
mgr.add_command("mc", MigrateCommand)


@app.route('/')
def index():

    return "index"


if __name__ == '__main__':
   mgr.run()