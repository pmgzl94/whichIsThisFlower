from flask import Flask
from flask import send_file
from flask import jsonify
from flask_graphql_auth import GraphQLAuth
from flask_graphql import GraphQLView
from flask_jwt import JWT

from graphql import GraphQLError
from graphene_file_upload.flask import FileUploadGraphQLView
import os
from PIL import Image

import SessionManager
from schema import schema

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "jwt-secret-key"
app.config["REFRESH_EXP_LENGTH"] = 30
app.config["ACCESS_EXP_LENGTH"] = 10

############################ TODO comment, only used to test on browser
# from flask_cors import CORS
# CORS(app) # This will enable CORS for all routes
#####################################################################

auth = GraphQLAuth(app)

# app.add_url_rule(
#     "/graphql", view_func=GraphQLView.as_view(
#         "graphql", schema=schema, graphiql=True
#     )
# )

app.add_url_rule(
    '/graphql',
    view_func=FileUploadGraphQLView.as_view(
        "graphql", schema=schema, graphiql=True
    )
)

@app.route('/download/<name>')
def download_file(name):
    path = "./cache/" + name
    print(path)
    try:
        if os.stat(path).st_size == 0:
            raise InvalidUsage('wrong type', status_code=400)
        Image.open(path)
    except:
        raise InvalidUsage('wrong format', status_code=400)
    return send_file(path, as_attachment=True)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
