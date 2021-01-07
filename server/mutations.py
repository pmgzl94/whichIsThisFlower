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
        print("[MUTATION]: [CreateUser]: mutate: user: {}, password: {}".format(username, password), file=sys.stderr)

        person = ObjectTypes.User(username=username)
        ok = True
        try:
            db.dbMan.addUser(username, password)
        except Exception as e:
            print(e, file=sys.stderr)
            ok = False
            raise GraphQLError(e)
        #call db
        return CreateUser(person=person, ok=ok)


class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def mutate(cls, _, info, username, password):
        print("[MUTATION]: [AuthMutation]: mutate: user: {}, password: {}".format(username, password), file=sys.stderr)

        try:
            dbUser = db.dbMan.getUser(username)
            if dbUser == None or password != dbUser["password"]:
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


class LogoutMutation(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()

    ok = graphene.Field(ObjectTypes.ProtectedUnion)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info):
        print("[MUTATION]: [LogoutMutation]: mutate", file=sys.stderr)
        SessionManager.session.removeSession(get_jwt_identity())
        return LogoutMutation(ok=ObjectTypes.IsOk(ok=True))


class TakePicture(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()
        image = graphene.String()
        imageName = graphene.String()

    ok = graphene.Field(ObjectTypes.ProtectedUnion)
    flowerName = graphene.Field(ObjectTypes.ProtectedUnion)
    # flowerName = graphene.Field(lambda: ObjectTypes.GetFlowerName)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info, image, imageName):
        print("[MUTATION]: [TakePicture]: mutate", file=sys.stderr)
        username = ""
        flowerName = "jsp"
        comment = ""
        # SessionManager.session.removeSession(get_jwt_identity())
        # function to get the name of the flower
        # db.dbMan.addImage(imageName, image, username, flowerName, comment)
        return TakePicture(ok=ObjectTypes.IsOk(ok=True), flowerName=ObjectTypes.GetFlowerName(flowerName=flowerName))










#example of protected mutation
class ProtectedMutation(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()

    message = graphene.Field(ObjectTypes.ProtectedUnion)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info):
        print("[MUTATION]: [ProtectedMutation]: mutate", file=sys.stderr)
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
        print("[MUTATION]: [OtherProtectedMutation]: mutate", file=sys.stderr)
        print(get_jwt_identity())
        return OtherProtectedMutation(otherObj=ObjectTypes.OtherObject(value=5))


class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()


    new_token = graphene.String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _):
        print("[MUTATION]: [RefreshMutation]: mutate", file=sys.stderr)
        current_user = get_jwt_identity() #get the user
        return RefreshMutation(new_token=create_access_token(identity=current_user))
