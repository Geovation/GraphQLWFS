import requests
import os
import graphene
import json


def buildWFSQuery(count, typeNames, filters):
    payload = {
        'typeNames': typeNames,
        'count': count
    }

    if filters:
        # filters dictionary not empty
        propertyIsEqualTo = ""
        for propertyName, literal in filters.items():
            propertyIsEqualTo += """
                <PropertyIsEqualTo>
                    <PropertyName>{0}</PropertyName>
                    <Literal>{1}</Literal>
                </PropertyIsEqualTo>
            """.format(propertyName, literal)

        if propertyIsEqualTo != "":
            filter = "<Filter>" + propertyIsEqualTo + "</Filter>"
            payload["filter"] = filter
    return payload

def fetchFeaturesFromWFS(count, typeNames, filters):
    OS_KEY = os.getenv('OS_KEY', '????????')
    #Edit WFS API Endpoint address here
    wfsApiBaseUrl = "https://api.os.uk/features/v1/wfs?service=wfs&request=GetFeature&key={}&version=2.0.0&outputformat=geoJSON".format(
        OS_KEY)
    
    payload = buildWFSQuery(count, typeNames, filters)
    response = requests.get(wfsApiBaseUrl, params=payload)

    if (response.status_code != 200):
        payloader = print(">>>>>>>>>>>>>>>> payload", payload)
        urlResponse = print(">>>>>>>>>>>>>>>> url", response.url)
        txtResponse = print(">>>>>>>>>>>>>>>> text", response.text)
        headerResp = print(">>>>>>>>>>>>>>>> headers", response.headers)
        statusResp = print(">>>>>>>>>>>>>>>> status_code", response.status_code)
        return ["Error: Check your logs"]
    
    if ('features' in response.json()):
        return response.json()['features']
        
    else:
        return response.json()
        
# Getting started with GraphQL. In this way we can extract data from the query.
# TODO: Next step is to convert this in a proper query.

def create_filter_hello (propertyName, literal):
    filters = {}

    # Check for empty filter arguments
    if ( (propertyName.strip()) and (literal.strip()) ):
        filters[propertyName] = literal

    return filters

class Query(graphene.ObjectType):
    #Update hello field with valid typenames Zoomstack_Sites
    hello = graphene.List(graphene.String,
        count=graphene.Int(default_value=10),
        typeNames=graphene.String(default_value="osfeatures:Zoomstack_Sites"),
        propertyName=graphene.String(default_value=""),
        literal=graphene.String(default_value="")
    )

    zoomstackNames = graphene.String(
        first=graphene.Int(default_value=10),
        Name1=graphene.String(default_value="BRECON BEACONS NATIONAL PARK")
    )

    #   {
    #      hello(
    #         count: 5,
    #         propertyName: "Ward",
    #         literal: "Bottisham Ward",
    #         typeNames: "osfeatures:BoundaryLine_PollingDistrict"
    #     )
    # }
    def resolve_hello(self, info, count, typeNames, propertyName, literal):
        if (count >= 0 ):
            filters = create_filter_hello(propertyName, literal)
            return fetchFeaturesFromWFS(count, typeNames, filters)

        else:
            return ["Error: Count needs to be 0 or more"]
            
    #  {
    #      zoomstackNames(
    #          first: 5,
    #          Type: "National Park"
    #      )
    #  }
    def resolve_zoomstackNames(self, info, first, Name1):
        filters = {
            "Name1": Name1
        }
        return fetchFeaturesFromWFS(count=first, typeNames="osfeatures:Zoomstack_Names", filters=filters)


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
    graphQlQuery = request.data.decode('utf-8')
    schema = graphene.Schema(query=Query)
    result = schema.execute(graphQlQuery)

    #  TODO: error handling
    return result.data
