import requests
import os
import graphene

def fetchFeaturesFromWFS(count, typeNames, filters):
    OS_KEY = os.getenv('OS_KEY', '????????')
    wfsApiBaseUrl = "https://osdatahubapi.os.uk/OSFeaturesAPI/wfs/v1?service=wfs&request=GetFeature&key={}&version=2.0.0&outputformat=geoJSON".format(OS_KEY)
    payload = {
        'typeNames': typeNames,
        'count': count
    }
    # TODO: generate <Filter> from filters

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

    response = requests.get(wfsApiBaseUrl, params=payload)
    if response.status_code != 200:
        payloader = print(">>>>>>>>>>>>>>>> payload", payload)
        urlResponse = print(">>>>>>>>>>>>>>>> url", response.url)
        txtResponse = print(">>>>>>>>>>>>>>>> text", response.text)
        headerResp = print(">>>>>>>>>>>>>>>> headers", response.headers)
        statusResp = print(">>>>>>>>>>>>>>>> status_code", response.status_code)
        return payload

    return response.json()['features']
# Getting started with GraphQL. In this way we can extract data from the query.
# {
#     boundaryLinePollingDistrict (
#         first: 5
#         ward: "Bottisham Ward",
#         parish: "Brinkley CP"
#     )
# }
# TO DO: Next step is to convert this in a proper query.
class Query(graphene.ObjectType):
    hello = graphene.String(
        count=graphene.Int(default_value=10),
        typeNames=graphene.String(default_value="osfeatures:BoundaryLine_PollingDistrict"),
        propertyName=graphene.String(default_value=""),
        literal=graphene.String(default_value="")
    )
    boundaryLinePollingDistrict = graphene.String(
        first=graphene.Int(default_value=10),
        ward=graphene.String(default_value="Bottisham Ward"),
        parish=graphene.String(default_value="Brinkley CP")
    )
    # AYMAR selection
    highways_RoadLink = graphene.String(
        first=graphene.Int(default_value=10),
        AlternateIdentifierScheme=graphene.String(default_value="NSG Elementary Street Unit ID (ESU ID)"),
        Directionality=graphene.String(default_value="bothDirections"),
        FormOfWay=graphene.String(default_value="Single Carriageway")
    )

    def resolve_hello(self, info, count, typeNames, propertyName, literal):
        filters = {}
        filters[propertyName] = literal
        return fetchFeaturesFromWFS(count, typeNames, filters)

    def resolve_boundaryLinePollingDistrict(self, info, first, ward, parish):
        filters = {
            "ward": ward,
            "parish": parish
        }
        return  fetchFeaturesFromWFS(count=first, typeNames="osfeatures:BoundaryLine_PollingDistrict", filters=filters)

    # AYMAR resolve function for selected field
    # def resolve_highways_RoadLink(self, info, first, alternateIdentifierScheme, directionality, formOfWay):
    #     filters = {
    #         "alternateIdentifierScheme": alternateIdentifierScheme,
    #         "directionality": directionality,
    #         "formOfWay": formOfWay
    #     }
    #     return  fetchFeaturesFromWFS(count=first, typeNames="osfeatures:highways_RoadLink", filters=filters)

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
    graphQlQuery += '''
    {
       hello(
          count: 5,
          propertyName: "alternateIdentifierScheme",
          literal: "NSG Elementary Street Unit ID (ESU ID)",
          typeNames: "osfeatures:Highways_RoadLink"
          )
      }
    '''

   #   {
   #      hello(
   #         count: 5,
   #         propertyName: "Ward",
   #         literal: "Bottisham Ward",
   #         typeNames: "osfeatures:BoundaryLine_PollingDistrict"
   #     )
   # }

    schema = graphene.Schema(query=Query)

    result = schema.execute(graphQlQuery)

    #  TODO: error handling
    return result.data
