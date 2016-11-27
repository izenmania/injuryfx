from flask import Flask

myapp = Flask(__name__)
myapp.config.from_object('config')

from myapp import views
