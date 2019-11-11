import requests
from flask import escape
import json 



def graphqlwfs(url):
    url = "https://osdatahubapi.os.uk/OSFeaturesAPI/wfs/v1?service=wfs&request=GetFeature&typename=osfeatures:BoundaryLine_CommunityWard&key=pxKGVMtaA9X2382DdJA4h3hAi6mkXt60&version=2.0.0&outputformat=geoJSON"
    # &outputFormat=GEOJSON
    response = requests.get(url+ "&outputFormat=GEOJSON")
    # """HTTP Cloud Function.
    # Args:
    #     request (flask.Request): The request object.
    #     <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    # Returns:
    #     The response text, or any set of values that can be turned into a
    #     Response object using `make_response`
    #     <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    # """
    # request_json = request.get_json(silent=True)
    # request_args = request.args

    # if request_json and 'name' in request_json:
    #     name = request_json['name']
    # elif request_args and 'name' in request_args:
    #     name = request_args['name']
    # else:
    #     name = 'World'
    return response.json()["features"][0]


    
    # response = requests.get('https://api.github.com')
    # if response:
    #     print('Success!')
    # else:
    #     print('An error has occurred.')

    # def requestInputs(url):
    #     pass

# 'Hello {}! '.format(escape(name)) + 