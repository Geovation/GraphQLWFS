import requests

"""HTTP Cloud Function.
Args:
    request (flask.Request): The request object.
    <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
Returns:
    The response text, or any set of values that can be turned into a
    Response object using `make_response`
    <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
"""
def graphqlwfs(request):
    wfsApiBaseUrl = "https://osdatahubapi.os.uk/OSFeaturesAPI/wfs/v1?service=wfs&request=GetFeature&key=pxKGVMtaA9X2382DdJA4h3hAi6mkXt60&version=2.0.0&outputformat=geoJSON"
    # request_json = request.get_json(silent=True)
    typeNames = request.args.get("typeNames", default="")
    count = request.args.get("count", default=100)
    PropertyName = request.args.get("PropertyName", default="")
    propertyValue = request.args.get("propertyValue", default="")
    payload = {
        'typeNames': typeNames,
        'count': count
    }
    if property == "" or propertyValue == "":
        filter = """
            <Filter>
                <PropertyIsEqualTo>
                    <PropertyName>{0}</PropertyName>
                    <Literal>{1}</Literal>
                </PropertyIsEqualTo>
            </Filter>
        """.format(PropertyName, propertyValue)
        payload["filter"] = filter
    response = requests.get(wfsApiBaseUrl, params=payload)
    print(">>>>>>>>>>>>>>>> payload", payload)
    print(">>>>>>>>>>>>>>>> url", response.url)
    print(">>>>>>>>>>>>>>>> text", response.text)
    print(">>>>>>>>>>>>>>>> headers", response.headers)
    print(">>>>>>>>>>>>>>>> status_code", response.status_code)
    if status_code != 200:
        // TODO parse XML which is in response.text
        return "NO NO NOc ccccc"
    else:
        features = response.json()
        return features