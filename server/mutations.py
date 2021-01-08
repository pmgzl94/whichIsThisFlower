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

import cnn

from base64 import b64encode, b64decode
from graphene_file_upload.scalars import Upload

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
        print("\n[MUTATION]: [AuthMutation]: mutate: user: {}, password: {}".format(username, password), file=sys.stderr)

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
        print("\n[MUTATION]: [LogoutMutation]: mutate", file=sys.stderr)
        SessionManager.session.removeSession(get_jwt_identity())
        return LogoutMutation(ok=ObjectTypes.IsOk(ok=True))

import base64

class TakePicture(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()
        imageName = graphene.String()
        image = Upload(required=True)

    ok = graphene.Field(ObjectTypes.ProtectedUnion)
    flowerName = graphene.Field(ObjectTypes.ProtectedUnion)
    # flowerName = graphene.Field(lambda: ObjectTypes.GetFlowerName)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info, imageName, image, **kwargs):
        print("\n[MUTATION]: [TakePicture]: mutate", file=sys.stderr)
        # newImage = bytes(image, 'utf-8').decode()
        fullpath = "./cache/" + imageName
        file = open(fullpath, "w")
        file.write(image)
        # file.write(base64.decode(image))
        # file.write(newImage)
        file.close()

        flowerName = cnn.models.zf5model(fullpath) # function to get the name of the flower
# =======
#         try:
#             file = open("./cache/" + imageName, "w")
#             file.write("oo")
#             # file.write(image.read().decode())
#             # image.read()
#             # image.read().decode()
#             # file.write(base64.decode(image))
#             # file.write(newImage)
#             file.close()
#         except:
#             print("aa")

#         flowerName = "It is not a flower" # function to get the name of the flower
# >>>>>>> b66d1d930b5f65a484abb92953e1fd5a05f0fa7e
        username = get_jwt_identity()
        comment = "none"

        db.dbMan.addImage(imageName, image, username, flowerName, comment)
        return TakePicture(ok=ObjectTypes.IsOk(ok=True), flowerName=ObjectTypes.GetFlowerName(flowerName=flowerName))


# class UploadMutation(graphene.Mutation):
#     class Arguments:
#         file = Upload(required=True)

#     success = graphene.Boolean()

#     def mutate(self, info, file, **kwargs):
#         # do something with your file

#         return UploadMutation(success=True)









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
