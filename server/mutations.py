import graphene
import ObjectTypes
from flask_graphql_auth import (
    get_jwt_identity,
    get_raw_jwt,
    create_access_token,
    create_refresh_token,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
)
import SessionManager
import db
import sys
from graphql import GraphQLError

#mutation object
# https://docs.graphene-python.org/en/latest/types/mutations/

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()
    
    # fields to return
    ok = graphene.Boolean()
    person = graphene.Field(lambda: ObjectTypes.User)

    def mutate(root, info, username, password):
        print("here2")
        person = ObjectTypes.User(username=username)
        try:
            db.dbMan.addUser(username, password)
        except Exception as e:
            print(e, file=sys.stderr)
            raise GraphQLError(e)
        #call db
        ok = True
        return CreateUser(person=person, ok=ok)


class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def mutate(cls, _, info, username, password):
        print("here")
        try:
            if password != db.dbMan.getUser(username)["password"]:
                raise GraphQLError("[MUTATION]: [AuthMutation]: wrong password")#raise or print?
        except Exception as e:
            print(e, file=sys.stderr)
            raise GraphQLError(e)
        #call db or raise event
        tok = create_access_token(username)
        refrshTok = create_refresh_token(username)
        SessionManager.session.addNewSession(username, tok)
        # print(info.context["user"])
        # info.context["username"] = username
        return AuthMutation(
            access_token=tok,
            refresh_token=refrshTok,
        )

#example of protected mutation
class ProtectedMutation(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()

    message = graphene.Field(ObjectTypes.ProtectedUnion)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info):
        #check jwt
        
        return ProtectedMutation(
            message=ObjectTypes.MessageField(message="Protected mutation works")
        )


class OtherProtectedMutation(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()
    otherObj = graphene.Field(ObjectTypes.ProtectedUnion)
    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info):
        print("here")
        print(get_jwt_identity())
        return OtherProtectedMutation(otherObj=ObjectTypes.OtherObject(value=5))


class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _):
        current_user = get_jwt_identity() #get the user
        return RefreshMutation(new_token=create_access_token(identity=current_user))
