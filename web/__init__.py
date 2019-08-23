from flask import Flask, render_template, abort, g
from jinja2 import TemplateNotFound
from flask_cors import CORS
import os

from web.api import api

queue = None
app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": "*"
    }
})

app.register_blueprint(api)


def run(q):
    global queue
    queue = q
    app.run(host="0.0.0.0")


@app.before_request
def inject_queue():
    global queue
    g.queue = queue


@app.route("/")
def home():
    try:
        return render_template("index.html")
    except TemplateNotFound:
        abort(404)