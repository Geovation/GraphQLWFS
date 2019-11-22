import requests
from flask import Flask, escape, request
import json



def graphqlwfs(url):
    url = "https://osdatahubapi.os.uk/OSFeaturesAPI/wfs/v1?service=wfs&request=GetCapabilities&key=pxKGVMtaA9X2382DdJA4h3hAi6mkXt60&version=2.0.0"
    queryString = "&typenames=osfeatures:BoundaryLine_PollingDistrict&outputformat=geoJSON"
    # count = 100
    # property = "Ward"
    # propertyValue = "Ely North Ward"

    request_json = request.get_json(silent=True)
    request_args = request.args


    if 'count' in request_args:
        count = request_args['count']
    else:
        count = 100

    if request_json and 'property' in request_json:
        property = request_json['property']
    elif request_args and 'property' in request_args:
        property = request_args['property']
    else:
        property = ""

    if request_json and 'propertyValue' in request_json:
        if '&' in request_json['propertyValue']:
            propertyValue = request_json['propertyValue']
            propertyValue = propertyValue.replace(" & ", " ")
        propertyValue = request_json['propertyValue']
    elif request_args and 'propertyValue' in request_args:
        if '&' in request_args['propertyValue']:
            propertyValue = request_args['propertyValue']
            propertyValue = propertyValue.replace(" & ", " ")
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

    # query_has = False
    # if 'count' not in url :
    #     query_has = True

    # return features['features'][0]['properties']['County']
    # return str(query_has)

    return features
