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

        if (typeNames == "osfeatures:Topography_TopographicArea"):
            propertyIsEqualToList = ["", "", "", "", "", "", "", ""]
            propertyList = [False, False, False, False, False, False, False, False]
            multipleProperty = ""
            multiplePropertyCount = 0

            for element in filters:
                if (filters[element] != None):
                    
                    if (element == "TOID" or element == "theme" or element == "reasonForChange" or element == "descriptiveGroup" or element == "make"):
                        if (len(filters[element].strip()) != 0):
                            if (element == "TOID"):
                                propertyList[0] = True
                                propertyIsEqualToList.insert( 0, buildEqualToFilter(propertyName="TOID", literal=filters['TOID']) )

                            elif (element == "theme"):
                                propertyList[2] = True
                                propertyIsEqualToList.insert( 2, buildEqualToFilter(propertyName="theme", literal=filters['theme']) )
                                
                            elif (element == "reasonForChange"):
                                propertyList[4] = True
                                propertyIsEqualToList.insert( 4, buildEqualToFilter(propertyName="reasonForChange", literal=filters['reasonForChange']) )
                                
                            elif (element == "descriptiveGroup"):
                                propertyList[5] = True
                                propertyIsEqualToList.insert( 5, buildEqualToFilter(propertyName="descriptiveGroup", literal=filters['descriptiveGroup']) )

                            elif (element == "make"):
                                propertyList[6] = True
                                propertyIsEqualToList.insert( 6, buildEqualToFilter(propertyName="make", literal=filters['make']) )

                    else:
                        if (element == "featureCode"):
                            propertyList[1] = True
                            propertyIsEqualToList.insert( 1, buildEqualToFilter(propertyName="featureCode", literal=filters['featureCode']) )

                        elif (element == "calculatedAreaValue"):
                            propertyList[3] = True
                            propertyIsEqualToList.insert( 3, buildEqualToFilter(propertyName="calculatedAreaValue", literal=filters['calculatedAreaValue']) )

                        elif (element == "physicalLevel"):
                            propertyList[7] = True
                            propertyIsEqualToList.insert( 7, buildEqualToFilter(propertyName="physicalLevel", literal=filters['physicalLevel']) )
                    
            # Create property list inside the And tag
            for i in range(len(propertyList)):
                if propertyList[i]:

                    multiplePropertyCount = multiplePropertyCount + 1
                    multipleProperty = multipleProperty + propertyIsEqualToList[i]

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

class Query(graphene.ObjectType):

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
