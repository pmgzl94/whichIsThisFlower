from flask_graphql_auth import AuthInfoField
import graphene

class MessageField(graphene.ObjectType):
    message=graphene.String()

#related to other object mutation
class OtherObject(graphene.ObjectType):
    value = graphene.Int()

class ProtectedUnion(graphene.Union):
    class Meta:
        types = (MessageField, OtherObject, AuthInfoField)

    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)

class User(graphene.ObjectType):
    username = graphene.String()
    # password = graphene.String()
