import graphene
import graphql_jwt
import api_v1.schema
from api_v1.schema import contact, contact_detail, user

class Query(contact.Query, graphene.ObjectType):
    pass

class Mutation(contact.Mutation, user.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
