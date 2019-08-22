from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound

app = Flask(__name__)


@app.route("/")
def home():
    try:
        return render_template("index.html")
    except TemplateNotFound:
        abort(404)