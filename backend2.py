import os
from flask_script import Manager
from flask_migrate import Migrate, upgrade, MigrateCommand
from app import create_app, db

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app('default')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

print(app.config["SQLALCHEMY_DATABASE_URI"])

@app.cli.command('initdb')
def init_db():
    db.drop_all()
    db.create_all()