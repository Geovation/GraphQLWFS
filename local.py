from flask import Flask, request, json
from main import graphqlwfs

# the following code is tu run it locally. Just run "local.sh"
app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def local():
    # return graphqlwfs(request)
    return "Yes Yes"

if __name__ == '__main__':
    app.run(debug=True)
