import graphene
import mutations
import ObjectTypes
from flask_graphql_auth import query_jwt_required

class Mutation(graphene.ObjectType):
    createUser = mutations.CreateUser.Field()

    auth = mutations.AuthMutation.Field()
    refresh = mutations.RefreshMutation.Field()
    protected = mutations.ProtectedMutation.Field()
    getOtherObj = mutations.OtherProtectedMutation.Field() #tested protected query

    logout = mutations.LogoutMutation.Field()
    takePicture = mutations.TakePicture.Field()
    getPicture = mutations.GetPictures.Field()


class Query(graphene.ObjectType):
    protected = graphene.Field(type=ObjectTypes.ProtectedUnion, token=graphene.String())

    @query_jwt_required
    def resolve_protected(self, info):
        print("QUERY", file=sys.stderr)

        return ObjectTypes.MessageField(message="Hello World!")


schema = graphene.Schema(query=Query, mutation=Mutation)
