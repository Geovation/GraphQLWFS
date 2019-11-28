import requests
import os
import graphene


def fetchFeaturesFromWFS(count, typeNames, propertyName, literal):
    OS_KEY = os.getenv('OS_KEY', '????????')
    wfsApiBaseUrl = "https://osdatahubapi.os.uk/OSFeaturesAPI/wfs/v1?service=wfs&request=GetFeature&key={}&version=2.0.0&outputformat=geoJSON".format(OS_KEY)

    payload = {
        'typeNames': typeNames,
        'count': count
    }
    if propertyName != "" and literal != "":
        filter = """
                <Filter>
                    <PropertyIsEqualTo>
                        <PropertyName>{0}</PropertyName>
                        <Literal>{1}</Literal>
                    </PropertyIsEqualTo>
                </Filter>
            """.format(propertyName, literal)
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
  hello = graphene.String(
      count=graphene.Int(default_value=10),
      typeNames=graphene.String(default_value="osfeatures:BoundaryLine_PollingDistrict"),
      propertyName=graphene.String(default_value=""),
      literal=graphene.String(default_value="")
      )

  def resolve_hello(self, info, count, typeNames, propertyName, literal):
    return fetchFeaturesFromWFS(count, typeNames, propertyName, literal)

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
