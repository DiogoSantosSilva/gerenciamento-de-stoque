from app import db, app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import app_config, app_active
config = app_config[app_active]

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from model import Role, User,  Category, Product

if __name__ == '__main__':
    manager.run()


