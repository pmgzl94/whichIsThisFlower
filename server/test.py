from flask import Flask
import graphene
from flask_graphql_auth import (
    AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    get_raw_jwt,
    create_access_token,
    create_refresh_token,
    query_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
)
from flask_graphql import GraphQLView
from graphql import GraphQLError
import SessionManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "aaaaaaaaaa"  # change this!
app.config["REFRESH_EXP_LENGTH"] = 30
app.config["ACCESS_EXP_LENGTH"] = 10

auth = GraphQLAuth(app)

# class UserCreated(graphene.ObjectType):
#     user = graphene.Field(type=User, username=graphene.String(), password=graphene.String())
#     def resolve_user(self, _):
        #call db


#mutation object
# https://docs.graphene-python.org/en/latest/types/mutations/
class User(graphene.ObjectType):
    username = graphene.String()
    # password = graphene.String()

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    ok = graphene.Boolean()
    person = graphene.Field(lambda: User)

    def mutate(root, info, username, password):
        person = User(username=username)
        #call db
        ok = True
        return CreateUser(person=person, ok=ok)

class MessageField(graphene.ObjectType):
    message=graphene.String()

class ProtectedUnion(graphene.Union):
    class Meta:
        types = (MessageField, AuthInfoField)

    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)

class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def mutate(cls, _, info, username, password):
        print("here")
        #call db or raise event
        tok = create_access_token(username)
        refrshTok = create_access_token(username)
        SessionManager.session.addNewSession(username, tok)
        # print(info.context["user"])
        # info.context["username"] = username
        return AuthMutation(
            access_token=tok,
            refresh_token=refrshTok,
        )


class ProtectedMutation(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()

    message = graphene.Field(ProtectedUnion)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info):
        #check jwt
        
        return ProtectedMutation(
            message=MessageField(message="Protected mutation works")
        )


class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _):
        current_user = get_jwt_identity()
        return RefreshMutation(new_token=create_access_token(identity=current_user))


class Mutation(graphene.ObjectType):
    auth = AuthMutation.Field()
    refresh = RefreshMutation.Field()
    protected = ProtectedMutation.Field()

    createUser = CreateUser.Field()


class Query(graphene.ObjectType):
    protected = graphene.Field(type=ProtectedUnion, token=graphene.String())

    @query_jwt_required
    def resolve_protected(self, info):
        
        # raise GraphQLError('That email already exists')
        
        # raise Exception('That email already exists')
        # print(info)

        return MessageField(message="Hello World!")


schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(debug=True)

# "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNjA2NTc4MzE4LCJuYmYiOjE2MDY1NzgzMTgsImp0aSI6ImZhNThiMjAxLTIxY2QtNDQ3OS05NzljLTYzOWRkYmMzYzUzNiIsImlkZW50aXR5Ijoib3VpIiwiZXhwIjoxNjA2NTc5MjE4fQ.4461Nvgk8dPC1Sqyf9Fz6EUUp7ySfJtGFExLhsLkL1k"