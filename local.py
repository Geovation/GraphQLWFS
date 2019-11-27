from flask import Flask, request
from main import result

# the following code is tu run it locally. Just run "local.sh"
app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def local():
    return str(result.data['id'])

if __name__ == '__main__':
    app.run()
