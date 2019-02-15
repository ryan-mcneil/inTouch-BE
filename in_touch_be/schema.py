import graphene
import api_v1.schema

class Query(api_v1.schema.Query, graphene.ObjectType):
    pass

class Mutation(api_v1.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
