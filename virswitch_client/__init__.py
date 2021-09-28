from flask import Flask

app = Flask(__name__)
app.secret_key = 'key_key'

from virswitch_client import views
