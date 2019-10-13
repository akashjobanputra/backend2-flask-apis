import os
from flask_script import Manager
from flask_migrate import Migrate, upgrade, MigrateCommand
from app import create_app, db

f_app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(f_app, db)
manager = Manager(f_app)

manager.add_command('db', MigrateCommand)


@f_app.cli.command('deploy')
def upgrade_migrate():
    upgrade()


@f_app.cli.command('initdb')
def init_db():
    db.drop_all()
    db.create_all()


@f_app.cli.command('test')
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
