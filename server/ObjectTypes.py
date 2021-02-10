from flask_graphql_auth import AuthInfoField
import graphene

class IsOk(graphene.ObjectType):
    ok=graphene.Boolean()

class GetFlowerName(graphene.ObjectType):
    flowerName = graphene.String()

class GetFlowersPic(graphene.ObjectType):
    flowersPic = graphene.List(graphene.String)

class MessageField(graphene.ObjectType):
    message=graphene.String()

#related to other object mutation
class OtherObject(graphene.ObjectType):
    value = graphene.Int()

class ProtectedUnion(graphene.Union):
    class Meta:
        types = (IsOk, GetFlowerName, GetFlowersPic, MessageField, OtherObject, AuthInfoField)

    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)

class User(graphene.ObjectType):
    username = graphene.String()
    # password = graphene.String()

class GetToken(graphene.ObjectType):
    token = graphene.String()
