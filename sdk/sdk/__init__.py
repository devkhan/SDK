"""
The flask application package.
"""
from flask import Flask, render_template, request, jsonify

import json
from sdk.user import usr
from sdk.biodb import biodb
from . import config

app = Flask(__name__)


app.register_blueprint(biodb, url_prefix = '/db')
app.register_blueprint(usr, url_prefix = '/usr')