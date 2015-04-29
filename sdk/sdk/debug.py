from flask import Flask
from user import usr
from biodb import biodb, model as bio_model
from config import config

app = Flask(__name__)
app.register_blueprint(usr, url_prefix = '/usr')
app.register_blueprint(biodb, url_prefix = '/db')


print(bio_model.Manage().add("YO", ["1","2"], "he","fwzsd",False)) 