import os

from redis import Redis, RedisError
from flask import Blueprint, render_template, abort, make_response
from jinja2 import TemplateNotFound

# Connect to Redis
if os.getenv('PYTHON_ENV') == 'production':
    redis_host = 'redis'
else:
    redis_host = 'localhost'
redis = Redis(host=redis_host, db=0, socket_connect_timeout=2, socket_timeout=2)

static_files = Blueprint('static_files', __name__, template_folder='templates')

@static_files.route("/css/<file>")
def css(file):
    print(f"Requested css file {file}")
    with open(f"public/css/{file}") as resource:
        resp = make_response()
        resp.headers['Content-Type'] = 'text/css'
        resp.data = resource.read()
        return resp