import os

from flask import Blueprint, render_template, abort, redirect, url_for
from flask_wtf import FlaskForm
from jinja2 import TemplateNotFound
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

from webapp.db import db, User
from webapp.pw_crypt import bcrypt

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

login_page_controller = Blueprint('login', __name__, template_folder='templates')

@login_page_controller.route('/login', methods=['GET', 'POST'])
def login_form():
    create_admin_if_missing()

    form = LoginForm()
    if form.validate_on_submit():
        target_user = User.query.filter_by(username=form.username.data).first()
        target_password = target_user.password if target_user is not None else None
        if  target_password is not None and bcrypt.check_password_hash(target_password, form.password.data):
            return redirect(url_for('dashboard.dashboard_view'))

    if form.is_submitted():
        return render_template('login.html', login_form=form)
    else:
        try:
            return render_template('login.html', login_form=form)
        except TemplateNotFound:
            abort(404)

