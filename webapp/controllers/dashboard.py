
from flask import Blueprint, render_template, abort, redirect, url_for
from flask_security import login_required

dashboard_controller = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard_controller.route("/")
@login_required
def dashboard_view():
    return render_template('dashboard.html')