import requests
import os
import graphene
import json
def fetchFeaturesFromWFS(count, typeNames, filters):
    OS_KEY = os.getenv('OS_KEY', '????????')
    wfsApiBaseUrl = "https://api.os.uk/features/v1/wfs?service=wfs&request=GetFeature&key={}&version=2.0.0&outputformat=geoJSON".format(OS_KEY)
    payload = {
        'typeNames': typeNames,
        'count': count
    }

    #wfs filter query for the PropertyIsEqualTo operator
    propertyIsEqualTo = ""
    for propertyName, literal in filters.items():
        propertyIsEqualTo += """
            <PropertyIsEqualTo>
                <PropertyName>{0}</PropertyName>
                <Literal>{1}</Literal>
            </PropertyIsEqualTo>
        """.format(propertyName, literal)

    #wfs filter query for the PropertyIsLessThanOrEqualTo operator
    PropertyIsLessThanOrEqualTo = ""
    for propertyName, literal in filters.items():
        PropertyIsLessThanOrEqualTo += """
            <PropertyIsLessThanOrEqualTo>
                <PropertyName>{0}</PropertyName>
                <Literal>{1}</Literal>
            </PropertyIsLessThanOrEqualTo>
        """.format(propertyName, literal)

    #Adds filter to payload array of url parameters
    if propertyIsEqualTo != "":
        filter = "<Filter>" + propertyIsEqualTo + "</Filter>"
        # payload["filter"] = filter

    #Adds another filter to payload array of url parameters
    if PropertyIsLessThanOrEqualTo != "":
        filter = "<Filter>" + PropertyIsLessThanOrEqualTo + "</Filter>"
        payload["filter"] = filter

    response = requests.get(wfsApiBaseUrl, params=payload)
    if response.status_code != 200:
        payloader = print(">>>>>>>>>>>>>>>> payload", payload)
        urlResponse = print(">>>>>>>>>>>>>>>> url", response.url)
        txtResponse = print(">>>>>>>>>>>>>>>> text", response.text)
        headerResp = print(">>>>>>>>>>>>>>>> headers", response.headers)
        statusResp = print(">>>>>>>>>>>>>>>> status_code", response.status_code)
        return "Error: Check your logs"
    return response.json()['features']

# Getting started with GraphQL. In this way we can extract data from the query.
# TODO: Next step is to convert this in a proper query.
class Query(graphene.ObjectType):
    #Field definition for Zoomstack_Airports feature
    ZoomstackAirports = graphene.String(
        count=graphene.Int(default_value=10),
        typeNames=graphene.String(default_value="osfeatures:Zoomstack_Airports"),
        propertyName=graphene.String(default_value=""),
        literal=graphene.String(default_value="")
    )

    #Field definition for zoomstack_Names feature
    zoomstackNames = graphene.String(
        first=graphene.Int(default_value=10),
        Name1=graphene.String(default_value="BRECON BEACONS NATIONAL PARK")
    )

    #Field definition for Zoomstack_Sites feature
    ZoomstackSites = graphene.String(
        first=graphene.Int(default_value=10),
        typeNames=graphene.String(default_value="osfeatures:Zoomstack_Sites"),
        propertyName=graphene.String(default_value=""),
        literal=graphene.Int(default_value=0)
    )

    #Resolver function for the field type ZoomstackAirports
    def resolve_ZoomstackAirports(self, info, count, typeNames, propertyName, literal):
        filters = {}
        filters[propertyName] = literal
        return fetchFeaturesFromWFS(count, typeNames, filters)

    #Resolver function for the field type zoomstackNames
    def resolve_zoomstackNames(self, info, first, Name1):
        filters = {
            "Name1": Name1
        }
        return  fetchFeaturesFromWFS(count=first, typeNames="osfeatures:Zoomstack_Names", filters=filters)

    #Resolver function for the field type ZoomstackSites
    def resolve_ZoomstackSites(self, info, first, typeNames, propertyName, literal):
        filters = {}
        filters[propertyName] = literal
        return  fetchFeaturesFromWFS(count=first, typeNames="osfeatures:Zoomstack_Sites", filters=filters)

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
    # graphQlQuery = request.data.decode('utf-8')

    #GraphQL query example 1
    graphQlQuery1 = """{
        ZoomstackAirports(
            count: 50,
            propertyName: "NAME",
            literal: "Sumburgh Airport",
            typeNames: "osfeatures:Zoomstack_Airports"
        )
    }"""

    #GraphQL query example 2
    graphQlQuery = """{
        ZoomstackSites(
            first: 8,
            typeNames: "osfeatures:Zoomstack_Sites",
            propertyName: "SHAPE_Area",
            literal: 2463
        )
    }"""
    schema = graphene.Schema(query=Query)
    result = schema.execute(graphQlQuery)

    #  TODO: error handling
    if result.errors != None:
        return "Your query did not execute"
    return result.data
