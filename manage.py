from flask_script import Manager,Server
from app.models import User
from flask_migrate import Migrate, MigrateCommand
from app import create_app,db

app = create_app('development')


manager =  Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
manager.add_command('server', Server)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User)

@manager.command
def test():
    '''
    Run the unit tests
    '''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=5).run(tests)

if __name__ == '__main__':

    manager.run()