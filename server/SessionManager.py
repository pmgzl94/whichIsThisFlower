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
    def removeSession(self, token):
        for (name, tok) in self.refs.items():
            if tok == token:
                self.refs.pop("name", None)
                return
        raise Exception("token not exists")
        

session = SessionManager()
