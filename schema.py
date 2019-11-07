import graphene

class Query(graphene.ObjectType):
    is_staff = graphene.Boolean()


    def resolve_is_staff(self, info):
        return True


schema = graphene.Schema(query=Query)

result = schema.execute(
    '''
    {
        isStaff
    }
    '''
)

print(result.data.items)
