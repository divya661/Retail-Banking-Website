import os
from flask import Flask, session, redirect, url_for,render_template
from flask_sqlalchemy import SQLAlchemy


# instance relative config makes flask look for configs in the instance folder in the root of the project
app = Flask(__name__, instance_relative_config=True)

# Assume environment to be dev if not specified
app.config['ENV'] = os.environ.get('FLASK_ENV', 'development')
app.secret_key = 'POJPIJIN#)@_!#(($)()9929!@onwoienfoi'


CONFIG_FILE = 'config_dev.json'

if app.config['ENV'] == 'production':
    CONFIG_FILE = 'config_prod.json'

app.config.from_json(CONFIG_FILE)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{username}:{password}@{server}'.format(
    username=app.config['DB_USERNAME'],  # FROM CONFIG
    password=app.config['DB_PASSWORD'],  # FROM CONFIG
    server=app.config['DB_SERVER'],  # FROM CONFIG
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


from .mod_auth import bp_auth, Employee
from .mod_customer import bp_customer, Customer
from .mod_account import bp_account, Account, AccountStatus

# db.drop_all()
db.engine.execute('CREATE DATABASE IF NOT EXISTS banking_application')
db.engine.execute('USE {database}'.format(database=app.config['DB_DATABASE']))
db.create_all()

app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_customer, url_prefix='/customer')
app.register_blueprint(bp_account, url_prefix='/account')

@app.route('/')
def site_root():
    employee_id = session.get('employee_id', False)
    username = session.get('username', False)

    if employee_id == False or username == False:
        return redirect(url_for('auth.login'))
    return redirect(url_for('customer.signup'))



