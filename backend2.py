import os
from flask_migrate import Migrate, upgrade, MigrateCommand
from app import create_app, db
from app.models import Machine, Tag, Cluster    # not used in this file, but still required so flask_migrate can work

f_app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(f_app, db)

f_app.cli.add_command('db', MigrateCommand)

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
