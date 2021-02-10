#!/usr/bin/python3
from pymongo import MongoClient
import sys

class dbManager():

    def __init__(self, addr, port, debug = False):
        self.refs = {}
        self.client = MongoClient(addr, port)
        self.db = self.client.db
        self.collection = self.db.user
        self.userPosts = self.db.userPosts
        self.imagePosts = self.db.imagePosts
        self.userImagePosts = self.db.userImagePosts
        self.debug = debug


# userPosts
    def addUser(self, userName, password):
        if self.debug == True:
            print("[DBMANAGER]: [addUser]: user : {}, password : {}".format(userName, password), file=sys.stderr)
        if self.getUser(userName) != None:
            raise Exception("[DBMANAGER]: [addUser]: user alredy exist")

        doc = {"username": userName,
               "password": password,
               "images": []}
        post_id = self.userPosts.insert_one(doc).inserted_id
        if self.debug == True:
            print("[DBMANAGER]: [addUser]: id : {}".format(post_id), file=sys.stderr)
            print("[DBMANAGER]: [addUser]: END", file=sys.stderr)
        return post_id

    def addImageToUser(self, user, image):
        if self.debug == True:
            print("[DBMANAGER]: [addImageToUser]: user : {}, image : {}".format(user, image), file=sys.stderr)
        userInfo = self.getUser(user)
        if userInfo == None:
            raise Exception("[DBMANAGER]: [addImageToUser]: user not found")

        arr = userInfo["images"]
        arr.append(image)
        result = self.userPosts.update_one(
            {"username" : user},
            {"$set":
             {"images": arr}
            }, upsert=True)
        if self.debug == True:
            print("[DBMANAGER]: [addImageToUser]: END", file=sys.stderr)
        if result.acknowledged != True:
            raise Exception("[DBMANAGER]: [addImageToUser]: set images failed")

    def deleteUser(self, user):
        if self.debug == True:
            print("[DBMANAGER]: [deleteUser]: user {}".format(user), file=sys.stderr)
        self.userPosts.delete_many({"username": user})

        if self.debug == True:
            print("[DBMANAGER]: [deleteUser]: END", file=sys.stderr)


    def getUser(self, name):
        if self.debug == True:
            print("[DBMANAGER]: [getUser]: user : {}".format(name), file=sys.stderr)
        user = self.userPosts.find_one({"username": name})

        if self.debug == True:
            if user != None:
                print (user, file=sys.stderr)
            print("[DBMANAGER]: [getUser]: END", file=sys.stderr)
        return user

    def getUsers(self):
        if self.debug == True:
            print("[DBMANAGER]: [getUsers]", file=sys.stderr)
        users = self.userPosts.find()

        if self.debug == True:
            if users != None:
                for user in users:
                    print (user, file=sys.stderr)
            print("[DBMANAGER]: [getUsers]: END", file=sys.stderr)
        return users

    def getNbUser(self):
        if self.debug == True:
            print("[DBMANAGER]: [getNbUsers]", file=sys.stderr)
        nb = self.userPosts.count_documents({})

        if self.debug == True:
            print("[DBMANAGER]: [getNbUsers]: nb: {}".format(nb), file=sys.stderr)
            print("[DBMANAGER]: [getNbUsers]: END", file=sys.stderr)
        return nb





# imagePosts
    def addImage(self, imageName, image, user, flowerName, comment):
        if self.debug == True:
            print("[DBMANAGER]: [addImage]: imageName : {}, flower : {}, user : {}, comment : {}".format(imageName, flowerName, user, comment), file=sys.stderr)
        if self.getImage(imageName) != None:
            raise Exception("[DBMANAGER]: [addImage]: image alredy exist")

        doc = {"imageName": imageName,
               "image": "oo",#image,
               "user": user,
               "flowerName": flowerName,
               "comment": comment}
        post_id = self.imagePosts.insert_one(doc).inserted_id
        if self.debug == True:
            print("[DBMANAGER]: [addImage]: id : {}".format(post_id), file=sys.stderr)
            print("[DBMANAGER]: [addImage]: END", file=sys.stderr)
        self.addImageToUser(user, imageName)
        return post_id

    def deleteImage(self, image):
        if self.debug == True:
            print("[DBMANAGER]: [deleteImages]: image {}".format(image), file=sys.stderr)
        self.imagePosts.delete_many({"imageName": image})

        if self.debug == True:
            print("[DBMANAGER]: [deleteImages]: END", file=sys.stderr)


    def getImage(self, name):
        if self.debug == True:
            print("[DBMANAGER]: [getImage]: image : {}".format(name), file=sys.stderr)
        image = self.imagePosts.find_one({"imagename": name})

        if self.debug == True:
            if image != None:
                print (image, file=sys.stderr)
            print("[DBMANAGER]: [getImage]: END", file=sys.stderr)
        return image

    def getImages(self):
        if self.debug == True:
            print("[DBMANAGER]: [getImages]", file=sys.stderr)
        images = self.imagePosts.find()

        if self.debug == True:
            if images != None:
                for image in images:
                    print (image, file=sys.stderr)
            print("[DBMANAGER]: [getImages]: END", file=sys.stderr)
        return images

    def getUserImages(self, name):
        if self.debug == True:
            print("[DBMANAGER]: [getUserImages]: user : {}".format(name), file=sys.stderr)
        images = self.imagePosts.find({"user": name})
        listImages = []

        if self.debug == True:
            if images != None:
                for image in images:
                    print (image, file=sys.stderr)
                    listImages.append(image["imageName"])
                # for image in listImages:
                #     print (image, file=sys.stderr)
            print("[DBMANAGER]: [getImages]: END", file=sys.stderr)
        return listImages


    def getNbImage(self):
        if self.debug == True:
            print("[DBMANAGER]: [getNbImages]", file=sys.stderr)
        nb = self.imagePosts.count_documents({})

        if self.debug == True:
            print("[DBMANAGER]: [getNbImages]: nb: {}".format(nb), file=sys.stderr)
            print("[DBMANAGER]: [getNbImages]: END", file=sys.stderr)
        return nb






# dbMan = dbManager("localhost", 27017)
dbMan = dbManager("localhost", 27017, True)






# dbMan.addUser("toto", "PPPPassword")
# dbMan.addUser("tata", "PPP")
# dbMan.getUser("tata")
# dbMan.getUser("toto")
# dbMan.getUser("titi")
# # dbMan.getUsers()
# dbMan.getNbUser()

# dbMan.addImage("best pic", "content", "toto", "rose", "no comment")
# dbMan.getNbImage()
# dbMan.getImages()
# dbMan.getUsers()
# dbMan.getUserImages("toto")
