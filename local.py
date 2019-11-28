from flask import Flask, request
from main import graphqlwfs

# the following code is tu run it locally. Just run "local.sh"
app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def local():
    return graphqlwfs(request)

if __name__ == '__main__':
    app.run()
