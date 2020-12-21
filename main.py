import requests
import os
import graphene
import json
import xmltodict


def build_query(count, typeNames, filters):
    payload = {
        'typeNames': typeNames,
        'count': count
    }

    if filters:
        # filters dictionary not empty

        if (typeNames == "Zoomstack_Sites"):
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
    
        elif (typeNames == "Zoomstack_Names"):
            propertyIsEqualToOne = ""
            propertyIsEqualToTwo = ""
            
            propertyIsEqualToOne = """
                <PropertyIsEqualTo>
                    <PropertyName>{0}</PropertyName>
                    <Literal>{1}</Literal>
                </PropertyIsEqualTo>
            """.format(filters['propertyName'], filters['literal'])
            
            if (filters['name1'].strip()):
                
                propertyIsEqualToTwo += """
                    <PropertyIsEqualTo>
                        <PropertyName>Name1</PropertyName>
                        <Literal>{0}</Literal>
                    </PropertyIsEqualTo>
                """.format(filters['name1'])
            
            if ((propertyIsEqualToOne != "") and (propertyIsEqualToTwo != "")):
                # Both properties are needed for filtering
                includingAnd = "<And>" + propertyIsEqualToOne + propertyIsEqualToTwo + "</And>"
                filter = "<Filter>" + includingAnd + "</Filter>"
                payload["filter"] = filter
            
            elif((propertyIsEqualToOne != "") and (propertyIsEqualToTwo == "")):
                # propertyName and literal filter are not empty
                filter = "<Filter>" + propertyIsEqualToOne + "</Filter>"
                payload["filter"] = filter
        
        elif (typeNames == "Zoomstack_RailwayStations"):
            propertyIsEqualToOne = ""
            propertyIsEqualToTwo = ""
            
            propertyIsEqualToOne = """
                <PropertyIsEqualTo>
                    <PropertyName>{0}</PropertyName>
                    <Literal>{1}</Literal>
                </PropertyIsEqualTo>
            """.format(filters['propertyName'], filters['literal'])
            
            if (filters['name'].strip()):
                
                propertyIsEqualToTwo += """
                    <PropertyIsEqualTo>
                        <PropertyName>Name</PropertyName>
                        <Literal>{0}</Literal>
                    </PropertyIsEqualTo>
                """.format(filters['name'])
            
            if ((propertyIsEqualToOne != "") and (propertyIsEqualToTwo != "")):
                # Both properties are needed for filtering
                includingAnd = "<And>" + propertyIsEqualToOne + propertyIsEqualToTwo + "</And>"
                filter = "<Filter>" + includingAnd + "</Filter>"
                payload["filter"] = filter
            
            elif((propertyIsEqualToOne != "") and (propertyIsEqualToTwo == "")):
                # propertyName and literal filter are not empty
                filter = "<Filter>" + propertyIsEqualToOne + "</Filter>"
                payload["filter"] = filter
        
        elif (typeNames == "Zoomstack_Airports"):
            propertyIsEqualTo = ""

            if (len(filters['name'].strip()) != 0):
                propertyIsEqualTo += """
                    <PropertyIsEqualTo>
                        <PropertyName>{0}</PropertyName>
                        <Literal>{1}</Literal>
                    </PropertyIsEqualTo>
                """.format( filters['propertyName'], filters['name'])

            if propertyIsEqualTo != "":
                filter = "<Filter>" + propertyIsEqualTo + "</Filter>"
                payload["filter"] = filter

    return payload

def get_feature(count, typeNames, filters):
    OS_KEY = os.getenv('OS_KEY', '????????')
    #Edit WFS API Endpoint address here
    wfsApiBaseUrl = "https://api.os.uk/features/v1/wfs?service=wfs&request=GetFeature&key={}&version=2.0.0&outputformat=geoJSON".format(
        OS_KEY)
    
    payload = build_query(count, typeNames, filters)
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

def get_capabilities():
    OS_KEY = os.getenv('OS_KEY', '????????')
    #Edit WFS API Endpoint address here
    wfsApiBaseUrl = "https://api.os.uk/features/v1/wfs?service=wfs&request=getcapabilities&key={}&version=2.0.0".format(
        OS_KEY)

    response = requests.get(wfsApiBaseUrl)
    if response.status_code != 200:
        urlResponse = print(">>>>>>>>>>>>>>>> url", response.url)
        txtResponse = print(">>>>>>>>>>>>>>>> text", response.text)
        headerResp = print(">>>>>>>>>>>>>>>> headers", response.headers)
        statusResp = print(">>>>>>>>>>>>>>>> status_code", response.status_code)
   
        errorMessage = {
            "wfs:WFS_Capabilities": "Error: Check your logs"
        }

        return xmltodict.unparse(errorMessage)
    return response.content

def describe_feature_type(typeNames):
    OS_KEY = os.getenv('OS_KEY', '????????')
    #Edit WFS API Endpoint address here
    wfsApiBaseUrl = "https://api.os.uk/features/v1/wfs?service=wfs&version=2.0.0&request=DescribeFeatureType&key={}".format(
        OS_KEY,)
    payload = {
        'typeNames': typeNames
    }

    response = requests.get(wfsApiBaseUrl, params=payload)
    if response.status_code != 200:
        urlResponse = print(">>>>>>>>>>>>>>>> url", response.url)
        txtResponse = print(">>>>>>>>>>>>>>>> text", response.text)
        headerResp = print(">>>>>>>>>>>>>>>> headers", response.headers)
        statusResp = print(">>>>>>>>>>>>>>>> status_code", response.status_code)
   
        errorMessage = {
            "xsd:schema": "Error: Check your logs"
        }

        return xmltodict.unparse(errorMessage)
    return response.content
        
# Getting started with GraphQL. In this way we can extract data from the query.
# TODO: Next step is to convert this in a proper query.

def create_filter_zoomstackSites (propertyName, literal):
    filters = {}

    # Check for empty filter arguments
    if ( (len(propertyName.strip()) != 0) and (len(literal.strip()) != 0) ):
        filters[propertyName] = literal

    return filters

class Query(graphene.ObjectType):

    getCapabilities = graphene.JSONString()

    describeFeatureType = graphene.JSONString(
        typeNames=graphene.String(required=True, default_value="")
    )

    zoomstackSites = graphene.List(graphene.String,
        count=graphene.Int(default_value=10),
        propertyName=graphene.String(default_value=""),
        literal=graphene.String(default_value="")
    )

    zoomstackNames = graphene.List(graphene.String,
        count=graphene.Int(default_value=10),
        propertyName=graphene.String(default_value=""),
        literal=graphene.String(default_value=""),
        name1=graphene.String(default_value=""),

    )

    zoomstackRailwayStations = graphene.List(graphene.String,
        count=graphene.Int(default_value=10),
        propertyName=graphene.String(default_value=""),
        literal=graphene.String(default_value=""),
        name=graphene.String(default_value=""),

    )

    zoomstackAirports = graphene.List(graphene.String,
        count=graphene.Int(default_value=10),
        propertyName=graphene.String(default_value=""),
        name=graphene.String(default_value=""),

    ) 

    # returns in json format after converting from xml received from WFS OS server
    def resolve_getCapabilities(self, info):
        responseOfGetCapabilities = get_capabilities()
        responseOfGetCapabilitiesInJSON = xmltodict.parse(responseOfGetCapabilities)
        return responseOfGetCapabilitiesInJSON
    
    # returns in json format after converting from xml received from WFS OS server
    def resolve_describeFeatureType(self, info, typeNames):

        if (len(typeNames.strip()) != 0):
            responseOfDescribeFeatureType = describe_feature_type(typeNames)
            responseOfDescribeFeatureTypeInJSON = xmltodict.parse(responseOfDescribeFeatureType)
            return responseOfDescribeFeatureTypeInJSON
        else:
            errorMessage = {"xsd:schema": "Error: typeNames parameter cannot be empty"
            }
            return errorMessage

    #   {
    #       zoomstackSites(
    #         count: 10,
    #         propertyName: "Type",
    #         literal: "Education",
    #     )
    # }
    def resolve_zoomstackSites(self, info, count, propertyName, literal):
        if (count >= 0 ):
            filters = create_filter_zoomstackSites(propertyName, literal)
            return get_feature(count = count, typeNames = "Zoomstack_Sites", filters = filters)

        else:
            return ["Error: Count needs to be 0 or more"]
            
    #  {
    #       zoomstackNames(
    #           count: 10,
    #           propertyName: "Type",
    #           literal: "City",
    #           name1: "Aberdeen",
    #       )
    #  }
    def resolve_zoomstackNames(self, info, count, propertyName, literal, name1):
        if (count >= 0 ):

            filters = {}
            # Check for empty filter arguments
            if ( (len(propertyName.strip()) != 0) and (len(literal.strip()) != 0) ):
                filters = {
                    "propertyName": propertyName,
                    "literal": literal,
                    "name1": name1
                }

        else:
            return ["Error: Count needs to be 0 or more"]
            
        return get_feature(count=count, typeNames="Zoomstack_Names", filters=filters)

    #  {
    #       zoomstackRailwayStations(
    #           count: 10,
    #           propertyName: "Name",
    #           literal: "Dunrobin Castle"
    #       )
    #  }
    def resolve_zoomstackRailwayStations(self, info, count, propertyName, literal, name):
        if (count >= 0 ):

            filters = {}
            # Check for empty filter arguments
            if ( (len(propertyName.strip()) != 0) and (len(literal.strip()) != 0) ):
                filters = {
                    "propertyName": propertyName,
                    "literal": literal,
                    "name": name
                }

        else:
            return ["Error: Count needs to be 0 or more"]
            
        return get_feature(count=count, typeNames="Zoomstack_RailwayStations", filters=filters)
    
    #  {
    #       zoomstackAirports(
    #           count: 10,
    #           propertyName: "Name",
    #           name: "Sumburgh Airport"
    #       )
    #  }
    def resolve_zoomstackAirports(self, info, count, propertyName, name):
        if (count >= 0 ):

            filters = {}
            # Check for empty filter arguments
            if ( (len(propertyName.strip()) != 0) and (len(name.strip()) != 0) ):
                filters = {
                    "propertyName": propertyName,
                    "name": name
                }

        else:
            return ["Error: Count needs to be 0 or more"]
            
        return get_feature(count=count, typeNames="Zoomstack_Airports", filters=filters)


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
