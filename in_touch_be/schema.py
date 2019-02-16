import graphene
import graphql_jwt
import api_v1.schema

class Query(api_v1.schema.Query, graphene.ObjectType):
    pass

class Mutation(api_v1.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
