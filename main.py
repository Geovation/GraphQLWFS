from flask import Flask, escape, request 
import requests
import json 



def graphqlwfs(url):
    url = "https://osdatahubapi.os.uk/OSFeaturesAPI/wfs/v1?service=wfs&request=GetCapabilities&key=pxKGVMtaA9X2382DdJA4h3hAi6mkXt60&version=2.0.0"
    queryString = "&typenames=osfeatures:BoundaryLine_PollingDistrict&outputformat=geoJSON"


   

   
    request_json = request.get_json(silent=True)
    request_args = request.args

    
    if request_json and 'count' in request_json:
        count = request_json['count']
    elif request_args and 'count' in request_args:
        count = request_args['count']
    else:
        count = 4000

    if request_json and 'property' in request_json:
        property = request_json['property']
    elif request_args and 'property' in request_args:
        property = request_args['property']
    else:
        property = ""

    if request_json and 'propertyValue' in request_json:
        propertyValue = request_json['propertyValue']
    elif request_args and 'propertyValue' in request_args:
        propertyValue = request_args['propertyValue']
    else:
        propertyValue = ""

    
    filterString = "&filter=<Filter><PropertyIsEqualTo><PropertyName>" + str(property) + "</PropertyName><Literal>" + str(propertyValue) + "</Literal></PropertyIsEqualTo></Filter>"

    if property == "":
        filterString = ""
    if propertyValue == "":
        filterString = ""
    
    
    newUrl = str(url.replace("GetCapabilities", "GetFeature") + queryString + "&count=" + str(count) + filterString)
    response = requests.get(newUrl)

    features = response.json()

    #  """HTTP Cloud Function.
    # Args:
    #     request (flask.Request): The request object.
    #     <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    # Returns:
    #     The response text, or any set of values that can be turned into a
    #     Response object using `make_response`
    #     <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    # """
    


    return features

      
        

            


   
    
