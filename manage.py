# -*- coding:utf8 -*-

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from ihome import create_app

app, db = create_app('develop')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
