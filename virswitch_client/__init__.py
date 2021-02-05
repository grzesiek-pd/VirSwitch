from flask import Flask

app = Flask(__name__)

from virswitch_client import views
