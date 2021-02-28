import sys
import graphene
from flask_graphql_auth import (
    get_jwt_identity,
    get_raw_jwt,
    create_access_token,
    create_refresh_token,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
)
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload

import ObjectTypes
import SessionManager
import db
sys.path.insert(1, './cnn/')
# sys.path.insert(2, './cnn/mnist')

import cnn.models
import cnn

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
        print("\n[MUTATION]: [CreateUser]: mutate: user: {}, password: {}".format(username, password), file=sys.stderr)

        person = ObjectTypes.User(username=username)
        ok = True
        try:
            db.dbMan.addUser(username, password)
        except Exception as e:
            print(e, file=sys.stderr)
            ok = False
            raise GraphQLError(e)
        return CreateUser(person=person, ok=ok)


class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def mutate(cls, _, info, username, password):
        print("\n[MUTATION]: [AuthMutation]: mutate: user: {}, password: {}".format(username, password), file=sys.stderr)

        try:
            dbUser = db.dbMan.getUser(username)
            if dbUser == None or password != dbUser["password"]:
                raise GraphQLError("[MUTATION]: [AuthMutation]: wrong password")
        except Exception as e:
            print(e, file=sys.stderr)
            raise GraphQLError(e)
        tok = create_access_token(username)
        refrshTok = create_refresh_token(username)
        SessionManager.session.addNewSession(username, tok)
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
        print("\n[MUTATION]: [LogoutMutation]: mutate", file=sys.stderr)
        SessionManager.session.removeSession(get_jwt_identity())
        return LogoutMutation(ok=ObjectTypes.IsOk(ok=True))

class TakePicture(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()
        imageName = graphene.String()
        image = Upload()

    ok = graphene.Field(ObjectTypes.ProtectedUnion)
    flowerName = graphene.Field(ObjectTypes.ProtectedUnion)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info, imageName, image, **kwargs):
        print("\n[MUTATION]: [TakePicture]: mutate", file=sys.stderr)
        fullPath = "./cache/" + imageName
        try:
            file = open(fullPath, "wb")
            file.write(image.read())
            file.close()
            print("IMAGE WRITEN")
        except:
            print("FAILED TO WRITE IMAGE")

        flowerName = cnn.models.flowerAndFunModel(fullPath)
        username = get_jwt_identity()
        comment = "none"

        db.dbMan.addImage(imageName, image, username, flowerName, comment)
        return TakePicture(ok=ObjectTypes.IsOk(ok=True), flowerName=ObjectTypes.GetFlowerName(flowerName=flowerName))

class GetPictures(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()

    ok = graphene.Field(ObjectTypes.ProtectedUnion)
    flowersPic = graphene.Field(ObjectTypes.ProtectedUnion)
    flowerNames = graphene.Field(ObjectTypes.ProtectedUnion)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info):
        print("\n[MUTATION]: [GetPictures]: mutate", file=sys.stderr)
        username = get_jwt_identity()
        flowersPic, flowerNames = db.dbMan.getUserImages(username)
        print("images:", flowersPic, file=sys.stderr)

        return GetPictures(ok=ObjectTypes.IsOk(ok=True), flowersPic=ObjectTypes.GetFlowersPic(flowersPic=flowersPic,flowerNames=flowerNames))










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
