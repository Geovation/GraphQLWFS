import requests
import os
import graphene
import json


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
        
# Getting started with GraphQL. In this way we can extract data from the query.
# TODO: Next step is to convert this in a proper query.

def create_filter_zoomstackSites (propertyName, literal):
    filters = {}

    # Check for empty filter arguments
    if ( (propertyName.strip()) and (literal.strip()) ):
        filters[propertyName] = literal

    return filters

class Query(graphene.ObjectType):

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
            if ( (propertyName.strip()) and (literal.strip()) ):
                filters = {
                    "propertyName": propertyName,
                    "literal": literal,
                    "name1": name1
                }

        else:
            return ["Error: Count needs to be 0 or more"]
            
        return get_feature(count=count, typeNames="Zoomstack_Names", filters=filters)


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
