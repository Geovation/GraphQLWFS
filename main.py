import requests
import os
import graphene
import json

def buildEqualToFilter(propertyName, literal):
    propertyIsEqualTo = """
                    <PropertyIsEqualTo>
                        <PropertyName>{0}</PropertyName>
                        <Literal>{1}</Literal>
                    </PropertyIsEqualTo>
                """.format(propertyName, literal)
    return propertyIsEqualTo
    
def buildWFSQuery(count, typeNames, filters):
    payload = {
        'typeNames': typeNames,
        'count': count
    }

    if filters:
        # filters dictionary not empty
        if (typeNames == "osfeatures:Zoomstack_Sites"):
            propertyIsEqualTo = ""
            for propertyName, literal in filters.items():
                propertyIsEqualTo += buildEqualToFilter(propertyName=propertyName, literal=literal)

            if propertyIsEqualTo != "":
                payload["filter"] = "<Filter>" + propertyIsEqualTo + "</Filter>"
        
        elif (typeNames == "osfeatures:Zoomstack_Names"):
            propertyIsEqualTo = ""
            for propertyName, literal in filters.items():
                propertyIsEqualTo += buildEqualToFilter(propertyName=propertyName, literal=literal) 

            if propertyIsEqualTo != "":
                payload["filter"] = "<Filter>" + propertyIsEqualTo + "</Filter>"

        elif (typeNames == "osfeatures:Topography_TopographicArea"):
            propertyIsEqualToList = ["", "", "", "", "", "", "", ""]
            propertyList = [False, False, False, False, False, False, False, False]
            multipleProperty = ""
            multiplePropertyCount = 0

            if ( filters['TOID'] != None ):
                if (len(filters['TOID'].strip()) != 0):
                    propertyList[0] = True
                    propertyIsEqualToList.insert( 0, buildEqualToFilter(propertyName="TOID", literal=filters['TOID']) )


            if ( filters['featureCode'] != None ):
                    propertyList[1] = True
                    propertyIsEqualToList.insert( 1, buildEqualToFilter(propertyName="featureCode", literal=filters['featureCode']) )

            if ( filters['theme'] != None ):
                if (len(filters['theme'].strip()) != 0):
                    propertyList[2] = True
                    propertyIsEqualToList.insert( 2, buildEqualToFilter(propertyName="theme", literal=filters['theme']) )
   
            if ( filters['calculatedAreaValue'] != None ):
                    propertyList[3] = True
                    propertyIsEqualToList.insert( 3, buildEqualToFilter(propertyName="calculatedAreaValue", literal=filters['calculatedAreaValue']) )
  
            if ( filters['reasonForChange'] != None ):
                if (len(filters['reasonForChange'].strip()) != 0):
                    propertyList[4] = True
                    propertyIsEqualToList.insert( 4, buildEqualToFilter(propertyName="reasonForChange", literal=filters['reasonForChange']) )

            if ( filters['descriptiveGroup'] != None ):
                if (len(filters['descriptiveGroup'].strip()) != 0):
                    propertyList[5] = True
                    propertyIsEqualToList.insert( 5, buildEqualToFilter(propertyName="descriptiveGroup", literal=filters['descriptiveGroup']) )

            if ( filters['make'] != None ):
                if (len(filters['make'].strip()) != 0):
                    propertyList[6] = True
                    propertyIsEqualToList.insert( 6, buildEqualToFilter(propertyName="make", literal=filters['make']) )
            
            if ( filters['physicalLevel'] != None ):
                    propertyList[7] = True
                    propertyIsEqualToList.insert( 7, buildEqualToFilter(propertyName="physicalLevel", literal=filters['physicalLevel']) )

            # Create property list inside the And tag
            for i in range(len(propertyList)):
                if propertyList[i]:

                    if (i == 0):
                        multiplePropertyCount = multiplePropertyCount + 1
                        multipleProperty = multipleProperty + propertyIsEqualToList[0]
                    elif (i == 1):
                        multiplePropertyCount = multiplePropertyCount + 1
                        multipleProperty = multipleProperty + propertyIsEqualToList[1]
                    elif (i == 2):
                        multiplePropertyCount = multiplePropertyCount + 1
                        multipleProperty = multipleProperty + propertyIsEqualToList[2]
                    elif (i == 3):
                        multiplePropertyCount = multiplePropertyCount + 1
                        multipleProperty = multipleProperty + propertyIsEqualToList[3]
                    elif (i == 4):
                        multiplePropertyCount = multiplePropertyCount + 1
                        multipleProperty = multipleProperty + propertyIsEqualToList[4]
                    elif (i == 5):
                        multiplePropertyCount = multiplePropertyCount + 1
                        multipleProperty = multipleProperty + propertyIsEqualToList[5]
                    elif (i == 6):
                        multiplePropertyCount = multiplePropertyCount + 1
                        multipleProperty = multipleProperty + propertyIsEqualToList[6]
                    elif (i == 7):
                        multiplePropertyCount = multiplePropertyCount + 1
                        multipleProperty = multipleProperty + propertyIsEqualToList[7]

            if (multiplePropertyCount > 1):
                multipleProperty = "<And>" + multipleProperty + "</And>"

            payload["filter"] = "<Filter>" + multipleProperty + "</Filter>"
            
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

    topographyTopographicArea = graphene.List(graphene.String,
        first=graphene.Int(),
        toid=graphene.String(),
        featureCode=graphene.Int(),
        theme=graphene.String(),
        calculatedAreaValue=graphene.Float(),
        reasonForChange=graphene.String(),
        descriptiveGroup=graphene.String(),
        make=graphene.String(),
        physicalLevel=graphene.Int(),
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

    # {
    #      topographyTopographicArea(
    #         first: 5,
    #         toid: "osgb1000000000006",
    #         featureCode: 10021,
    #         theme: "Buildings",
    #         calculatedAreaValue: 46.68,
    #         reasonForChange: "Restructured",
    #         descriptiveGroup: "Building",
    #         make: "Manmade",
    #         physicalLevel: 50,
    #     )
    # }
    def resolve_topographyTopographicArea(self, info, first=1, toid=None, featureCode=None, theme=None, calculatedAreaValue=None, reasonForChange=None, descriptiveGroup=None, make=None, physicalLevel=None):
        if (first >= 0 or first == None):
            filters =  {
                "TOID": toid,
                "featureCode": featureCode,
                "theme": theme,
                "calculatedAreaValue": calculatedAreaValue,
                "reasonForChange": reasonForChange,
                "descriptiveGroup": descriptiveGroup,
                "make": make,
                "physicalLevel": physicalLevel
            }
        
        else:
            return ["Error: First needs to be 0 or more"]

        return fetchFeaturesFromWFS(count=first, typeNames="osfeatures:Topography_TopographicArea", filters=filters)



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
