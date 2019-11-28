import requests
import os
import graphene

"""HTTP Cloud Function.
Args:
    request (flask.Request): The request object.
    <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
Returns:
    The response text, or any set of values that can be turned into a
    Response object using `make_response`
    <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
"""

class Query(graphene.ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    first_name = graphene.String(name=graphene.String(default_value="Aymar"))
    last_name = graphene.String()
    id = graphene.Int()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_first_name(root, info, name):
        return f'Hello {name}!'

    def resolve_last_name(root, info):
        return 'See ya!'

    def resolve_id(root, info):
        return 5

schema = graphene.Schema(query=Query)
result = schema.execute('{ id }')
# print(result.data['id'])

# def graphqlwfs(request):
#
#     OS_KEY = os.getenv('OS_KEY', '????????')
#     wfsApiBaseUrl = "https://osdatahubapi.os.uk/OSFeaturesAPI/wfs/v1?service=wfs&request=GetFeature&key={}&version=2.0.0&outputformat=geoJSON".format(OS_KEY)
#     # request_json = request.get_json(silent=True)
#     typeNames = request.args.get("typeNames", default="osfeatures:BoundaryLine_PollingDistrict")
#     count = request.args.get("count", default=100)
#     PropertyName = request.args.get("PropertyName", default=None)
#     Literal = request.args.get("Literal", default=None)
#     payload = {
#         'typeNames': typeNames,
#         'count': count
#     }
#     if PropertyName != None and Literal != None:
#         filter = """
#                 <Filter>
#                     <PropertyIsEqualTo>
#                         <PropertyName>{0}</PropertyName>
#                         <Literal>{1}</Literal>
#                     </PropertyIsEqualTo>
#                 </Filter>
#             """.format(PropertyName, Literal)
#         payload["filter"] = filter
#     response = requests.get(wfsApiBaseUrl, params=payload)
#     payloader = print(">>>>>>>>>>>>>>>> payload", payload)
#     urlResponse = print(">>>>>>>>>>>>>>>> url", response.url)
#     txtResponse = print(">>>>>>>>>>>>>>>> text", response.text)
#     headerResp = print(">>>>>>>>>>>>>>>> headers", response.headers)
#     statusResp = response.status_code
#     if response.status_code != 200:
#         return "Please enter a typeName!!! " + str(urlResponse) + str(txtResponse) + str(headerResp) + str(PropertyName) + str(Literal) +str(payload)
#     else:
#         features = response.json()
#     return features
    # if status_code != 200:
    #     return "NOOOOOO!!!"
    # #     return response.json()
    # return response.json()
