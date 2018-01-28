# _*_ coding:utf-8 _*_
from flask_migrate import Migrate, MigrateCommand, Manager
from iHome import create_app, db

app = create_app("DevelopmentConig")
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)



if __name__ == "__main__":
    # 测试redis
    # redisstorge.set("name","laowang")
    # session['name'] = 'xiaohua'
    # app.run()
    manager.run()
