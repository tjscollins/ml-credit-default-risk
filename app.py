from flask import Flask
from redis import Redis, RedisError
import os
import socket

is_production_env = os.getenv('PYTHON_ENV') == 'production'

# Connect to Redis
if is_production_env:
    redis_host = 'redis'
else:
    redis_host = 'localhost'
redis = Redis(host=redis_host, db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    if is_production_env:
        print(f"Cannot run directly in production")
    else:
        app.run(host='0.0.0.0', port=3000)
