class SessionManager():
    def __init__(self):
        self.refs = {}
        self.expired = {}
    
    def addNewSession(self, username, token):
        print("new registered user: {} = {} ".format(username, token))
        self.refs[username] = token
    def checkSessionToken(self, token):
        for val in self.refs.values():
            if val == token:
                return True
        raise Exception("token not exists")
    def removeSession(self, username):
        if username in self.refs.keys():
            self.refs.pop(username, None)
        else:
            raise Exception("token not exists")
        

session = SessionManager()
