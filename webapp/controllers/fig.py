from datetime import timedelta
import os

from flask import Blueprint, Response
from flask_security import login_required
from werkzeug.wsgi import FileWrapper

from webapp.charts import most_important_features_chart, explained_variance_chart, top_correlations_chart

fig_controller = Blueprint('fig', __name__, template_folder='templates')

@fig_controller.route("/fig/top-importances.png")
@login_required
def top_importances():
    img = most_important_features_chart()
    img_file = FileWrapper(img)
    return Response(img_file, mimetype='image/png', direct_passthrough=True, content_type='image/png')

@fig_controller.route("/fig/explained-variance.png")
@login_required
def exp_variances():
    img = explained_variance_chart()
    img_file = FileWrapper(img)
    return Response(img_file, mimetype='image/png', direct_passthrough=True, content_type='image/png')

@fig_controller.route("/fig/top-correlation.png")
@login_required
def top_correlations():
    img = top_correlations_chart()
    img_file = FileWrapper(img)
    return Response(img_file, mimetype='image/png', direct_passthrough=True, content_type='image/png')
