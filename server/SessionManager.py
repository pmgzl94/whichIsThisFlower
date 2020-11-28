class SessionManager():

    def __init__(self):
        self.refs = {}
    
    def addNewSession(self, username, token):
        print("new registered user: {} = {} ".format(username, token))
        if username in self.refs:
            self.refs[username] = token
    def checkSessionToken(self, token):
        for val in self.refs.values():
            if val == token:
                return True
        raise Exception("token not exists")

session = SessionManager()
