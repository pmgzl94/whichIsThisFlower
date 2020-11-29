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



    def addUser(self, userName, password):
        doc = {"username": userName,
               "password": password}
        post_id = self.posts.insert_one(doc).inserted_id

    def getUser(self, name):
        user = self.posts.find_one({"username": name})
        return user


    def getNbUser(self):
        nb = self.posts.count_documents({})
        return nb
        
dbMan = dbManager("localhost", 27017)






dbMan.addUser("toto", "PPPPassword")
dbMan.addUser("tata", "PPP")
dbMan.getUser("tata")
dbMan.getUser("toto")
dbMan.getNbUser()



