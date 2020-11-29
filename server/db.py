#!/usr/bin/python3
from pymongo import MongoClient
import sys

class dbManager():

    def __init__(self, addr, port, debug = False):
        self.refs = {}
        self.client = MongoClient(addr, port)
        self.db = self.client.db
        self.collection = self.db.user
        self.posts = self.db.posts
        self.debug = debug



    def addUser(self, userName, password):
        if self.debug == True:
            print("[DBMANAGER]: [addUser]: user : {}, password : {} ".format(userName, password), file=sys.stderr)
        doc = {"username": userName,
               "password": password}
        post_id = self.posts.insert_one(doc).inserted_id
        if self.debug == True:
            print("[DBMANAGER]: [addUser]: id : {}".format(post_id), file=sys.stderr)
            print("[DBMANAGER]: [addUser]: END", file=sys.stderr)

    def getUser(self, name):
        if self.debug == True:
            print("[DBMANAGER]: [getUsers]: user : {}".format(name), file=sys.stderr)

        user = self.posts.find_one({"username": name})
        if self.debug == True:
            print (user, file=sys.stderr)
            print("[DBMANAGER]: [getUsers]: END")
        return user


    def getNbUser(self):
        if self.debug == True:
            print("[DBMANAGER]: [getUsers]", file=sys.stderr)

        nb = self.posts.count_documents({})
        if self.debug == True:
            print (nb)
            print("[DBMANAGER]: [getUsers]: END", file=sys.stderr)
        return nb

# dbMan = dbManager("localhost", 27017)
dbMan = dbManager("localhost", 27017, True)






dbMan.addUser("toto", "PPPPassword")
dbMan.addUser("tata", "PPP")
dbMan.getUser("tata")
dbMan.getUser("toto")
dbMan.getNbUser()



