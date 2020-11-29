import graphene
import mutations
import ObjectTypes
from flask_graphql_auth import query_jwt_required

class Mutation(graphene.ObjectType):
    auth = mutations.AuthMutation.Field()
    refresh = mutations.RefreshMutation.Field()
    protected = mutations.ProtectedMutation.Field()
    getOtherObj = mutations.OtherProtectedMutation.Field() #tested protected query

    createUser = mutations.CreateUser.Field()


class Query(graphene.ObjectType):
    protected = graphene.Field(type=ObjectTypes.ProtectedUnion, token=graphene.String())

    @query_jwt_required
    def resolve_protected(self, info):
        
        # raise GraphQLError('That email already exists')
        
        # raise Exception('That email already exists')
        # print(info)

        return ObjectTypes.MessageField(message="Hello World!")


schema = graphene.Schema(query=Query, mutation=Mutation)
