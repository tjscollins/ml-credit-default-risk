import os
import socket

from flask import Flask, render_template, make_response
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, login_required

from webapp.db import db, user_datastore, User

from webapp.controllers.static_dev import static_files
from webapp.controllers.crsa import crsa_controller
from webapp.controllers.fig import fig_controller

is_production_env = os.getenv('PYTHON_ENV') == 'production'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECRET_KEY')

db.init_app(app)
migrate = Migrate(app, db)
security = Security(app, user_datastore)

app.register_blueprint(crsa_controller)
app.register_blueprint(fig_controller)

if not is_production_env:
    app.register_blueprint(static_files)

# Create an admin user if one does not exist
@app.before_first_request
def create_admin_if_missing():
    admin_user = User.query.filter_by(email='admin@bank.co').first()
    if admin_user is None:
        db.create_all()
        admin_password = os.environ.get('ADMIN_PASSWORD')
        user_datastore.create_user(email='admin@bank.co', password=admin_password)
        db.session.commit()

if __name__ == "__main__":
    if is_production_env:
        print(f"Cannot run directly in production")
        exit(1)
    else:
        app.run(host='0.0.0.0', port=8000)
