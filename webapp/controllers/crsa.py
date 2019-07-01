from datetime import timedelta
import os

from flask import Blueprint, render_template, abort, redirect, url_for, request, session
from flask_security import login_required
from wtforms import Form, SelectField, SubmitField
from wtforms.csrf.session import SessionCSRF
import numpy as np
import pandas as pd

from webapp.settings import SITE_TITLE
from webapp.cdm import test_data, raw_data, column_descriptions, model_prediction

APP_REVIEW_TITLE = 'Credit Risk Score Application: Application Review'
ANALYTICS_TITLE= 'Credit Risk Score Application: Application Analytics'

class MyBaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = bytes(os.environ.get('SECRET_KEY', default=''), 'utf-8')
        csrf_time_limit = timedelta(minutes=20)

        @property
        def csrf_context(self):
            return session

crsa_controller = Blueprint('crsa', __name__, template_folder='templates')

test_data['SK_ID_CURR'] = test_data.index
current_applicant_ids = np.array(test_data.index)

class SelectApplicantForm(MyBaseForm):
    id = SelectField(
        label='Applicant ID',
        choices=[(ID, ID) for ID in test_data.index[:1000]]
    )
    submit = SubmitField(label='Submit')

@crsa_controller.route("/")
@login_required
def dashboard_view():
    select_applicant_form = SelectApplicantForm()
    loan_applicants = []

    return render_template(
        'crsa/index.html',
        site_title=SITE_TITLE,
        page_title=APP_REVIEW_TITLE,
        select_applicant_form=select_applicant_form
    )

@crsa_controller.route("/crsa/view-applicant")
@login_required
def select_applicant():
    applicant_id = request.args.get('id')
    select_applicant_form = SelectApplicantForm(id=applicant_id)
    select_applicant_form.submit.name = ''

    applicant_data = [
        (
            col,
            column_descriptions.iloc[0][col], 
            raw_data[raw_data['SK_ID_CURR'] == int(applicant_id)].iloc[0][col]
        ) for col in raw_data.columns
    ]

    data = pd.DataFrame(test_data.drop(labels=['SK_ID_CURR'], axis=1).loc[int(applicant_id)][:]).T

    prediction = model_prediction(data)

    selected_applicant = { 
        'id': applicant_id,
        'data': applicant_data
    }

    return render_template(
        'crsa/index.html',
        site_title=SITE_TITLE,
        page_title=APP_REVIEW_TITLE,
        select_applicant_form=select_applicant_form,
        selected_applicant=selected_applicant,
        prediction=prediction,
        request=request
    )

@crsa_controller.route("/crsa/view-analytics")
@login_required
def application_analytics():
    return render_template(
        'crsa/index.html',
        site_title=SITE_TITLE,
        page_title=ANALYTICS_TITLE,
        selected_applicant={},
        request=request
    )