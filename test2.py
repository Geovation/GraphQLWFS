# Imports
from flask import Flask
# app initialization
app = Flask(__name__)
app.debug = True
# Configs
# TO-DO
# Modules
# TO-DO
# Models
# TO-DO
# Schema Objects
# TO-DO
# Routes
# TO-DO
@app.route('/')
def index():
    return '<p> Hello John</p>'
if __name__ == '__main__':
     app.run()