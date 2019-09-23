
from run import app
# import app

from models.modles import db
#数据库迁移包
from flask_migrate import Migrate,MigrateCommand
#脚本管理器
from flask_script import Manager

#映入数据库配置文件
app.config.from_object("db_config")
manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command("db",MigrateCommand)

if __name__ == '__main__':
    manager.run()