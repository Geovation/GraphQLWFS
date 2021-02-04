import requests
import os
import graphene
import json
import constant

# build_filter_property_is_equal_to builds PropertyIsEqualTo block item which would later be enclosed in Filter tag.
def build_filter_property_is_equal_to(propertyName, literal):
    propertyIsEqualTo = """
                    <PropertyIsEqualTo>
                        <PropertyName>{0}</PropertyName>
                        <Literal>{1}</Literal>
                    </PropertyIsEqualTo>
                """.format(propertyName, literal)
    return propertyIsEqualTo

# build_filter_property_is_less_than builds PropertyIsLessThan block item which would later be enclosed in Filter tag.
def build_filter_property_is_less_than(propertyName, literal):
    propertyIsLessThan = """
                    <PropertyIsLessThan>
                        <PropertyName>{0}</PropertyName>
                        <Literal>{1}</Literal>
                    </PropertyIsLessThan>
                """.format(propertyName, literal)
    return propertyIsLessThan

# call_build_filter_item creates property conditional block depending on the custom filterTag variable provided by the client.
def call_build_filter_item(propertyName, literal, filterTag):
    propertyString = ""

    if ( filterTag == "PropertyIsEqualTo" or filterTag == "_eq"):
        propertyString = build_filter_property_is_equal_to(propertyName, literal)

    elif( filterTag == "PropertyIsNotEqualTo" or filterTag == "_neq" ):
        print("PropertyIsNotEqualTo")

    elif( filterTag == "PropertyIsLessThan" or filterTag == "_lt" ):
        propertyString = build_filter_property_is_less_than(propertyName, literal)

    elif( filterTag == "PropertyIsGreaterThan" or filterTag == "_gt" ):
        print("PropertyIsGreaterThan")

    elif( filterTag == "PropertyIsLessThanOrEqualTo" or filterTag == "_lte" ):
        print("PropertyIsLessThanOrEqualTo")

    elif( filterTag == "PropertyIsGreaterThanOrEqualTo" or filterTag == "_gte" ):
        print("PropertyIsGreaterThanOrEqualTo")

    elif( filterTag == "PropertyIsLike" or filterTag == "_like" ):
        print("PropertyIsLike")

    elif( filterTag == "PropertyIsBetween" ):
        print("PropertyIsBetween")
    
    return propertyString

# build_filter_tag_topograhy_topographic_area creates the filter tag only for topographyTopographicArea API call.
def build_filter_tag_topograhy_topographic_area(filters):
    
    propertyInsideFilterTagDict = {
        "TOID": "",
        "featureCode": "",
        "theme": "",
        "calculatedAreaValue": "",
        "reasonForChange": "",
        "descriptiveGroup": "",
        "make": "",
        "physicalLevel": "",
    }

    propertyDict = {
        "TOID": False,
        "featureCode": False,
        "theme": False,
        "calculatedAreaValue": False,
        "reasonForChange": False,
        "descriptiveGroup": False,
        "make": False,
        "physicalLevel": False,
    }
    multipleProperty = ""
    multiplePropertyCount = 0

    for element in filters:
        if (filters[element] != None):
                    
            if (element == "TOID" or element == "theme" or element == "reasonForChange" or element == "descriptiveGroup" or element == "make"):
                if (len(filters[element].strip()) != 0):
                    propertyDict[element] = True
                    propertyInsideFilterTagDict[element] = call_build_filter_item(propertyName=element, literal=filters[element], filterTag=filters['filterTag'])

            elif(element == "featureCode" or element == "calculatedAreaValue" or element == "physicalLevel"):
                propertyDict[element] = True
                propertyInsideFilterTagDict[element] = call_build_filter_item(propertyName=element, literal=filters[element], filterTag=filters['filterTag'])

    # Loop through to build the filter conditional block items
    for i in propertyDict:
        if (propertyDict[i]):
            multiplePropertyCount = multiplePropertyCount + 1
            multipleProperty = multipleProperty + propertyInsideFilterTagDict[i]
    
    # Check whether to add And tag if multiple filter block item are present
    if (multiplePropertyCount > 1):
        multipleProperty = "<And>" + multipleProperty + "</And>"
    
    # Check whether to add Filter tag whether filtering was required by client
    if (len(multipleProperty.strip()) != 0):
        filter = "<Filter>" + multipleProperty + "</Filter>"
    else:
        filter = ""

    return filter


# build_wfs_query creates the payload including the filter tag for all the API call.
def build_wfs_query(count, typeNames, filters):
    payload = {
        'typeNames': typeNames,
        'count': count
    }

    if filters:
        # filters dictionary not empty
    
        if (typeNames == "osfeatures:Topography_TopographicArea"):

            filter = build_filter_tag_topograhy_topographic_area(filters)

            if (len(filter.strip()) != 0):
                payload["filter"] = build_filter_tag_topograhy_topographic_area(filters)
           
    return payload

# fetch_feature_from_wfs sends request and receives results from the WFS server once the http link is parsed which includes API key, payload, count, typeNames.
def fetch_feature_from_wfs(count, typeNames, filters):
    OS_KEY = os.getenv('OS_KEY', '????????')
    #Edit WFS API Endpoint address here
    wfsApiBaseUrl = "https://api.os.uk/features/v1/wfs?service=wfs&request=GetFeature&key={}&version=2.0.0&outputformat=geoJSON".format(
        OS_KEY)
    
    payload = build_wfs_query(count, typeNames, filters)
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

# Query class defines the GraphQL query and the corresponding resolve function as well.
class Query(graphene.ObjectType):
    
    #topographyTopographicArea = graphene.List(graphene.String,
    #    first=graphene.Int(),
    #    toid=graphene.String(),
    #    featureCode=graphene.Int(),
    #    theme=graphene.String(),
    #    calculatedAreaValue=graphene.Float(),
    #    reasonForChange=graphene.String(),
    #    descriptiveGroup=graphene.String(),
    #    make=graphene.String(),
    #    physicalLevel=graphene.Int(),
    #    filterTag=graphene.String(),
    #)

    topographyTopographicArea = graphene.List(graphene.String,
        filter=graphene.JSONString(),
        first=graphene.Int(),
        toid=graphene.String(),
        featureCode=graphene.Int(),
        theme=graphene.String(),
        calculatedAreaValue=graphene.Float(),
        reasonForChange=graphene.String(),
        descriptiveGroup=graphene.String(),
        make=graphene.String(),
        physicalLevel=graphene.Int(),
        filterTag=graphene.String()
        
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
    #         filterTag: "_eq"
    #     )
    # }
    # For less than filtering to trigger use:
    
    # { topographyTopographicArea( first: 1,  filter : { calculatedAreaValue : { _lt :  60.0 }  })  } 

    def resolve_topographyTopographicArea(self, info, filter={}, first=1, toid=None, featureCode=None, theme=None, calculatedAreaValue=None, reasonForChange=None, descriptiveGroup=None, make=None, physicalLevel=None, filterTag="_eq"):  

        if (first >= 0 or first == None):
            filters =  {
                "TOID": toid,
                "featureCode": featureCode,
                "theme": theme,
                "calculatedAreaValue": calculatedAreaValue,
                "reasonForChange": reasonForChange,
                "descriptiveGroup": descriptiveGroup,
                "make": make,
                "physicalLevel": physicalLevel,
            }

            if filter:
                for propertyName in filter:
                    for filterName in filter[propertyName]:
                        filters[propertyName] = filter[propertyName][filterName]
                        filters["filterTag"] = filterName

            elif filterTag in constant.GRAPHQL_FILTERTAG:
                # _conditional in GraphQL convention
                filters["filterTag"] = filterTag
            
            elif filterTag in constant.FILTERTAG:
                # conditional with respect to OGC standard
                filters["filterTag"] = filterTag
            
            else:
                return ["Error: Please check filterTag parameter, could not find the operator provided"]

        else:
            return ["Error: First needs to be 0 or more"]

        return fetch_feature_from_wfs(count=first, typeNames="osfeatures:Topography_TopographicArea", filters=filters)



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
