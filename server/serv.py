from flask import Flask
import graphene
from flask_graphql_auth import GraphQLAuth
from flask_graphql import GraphQLView
from graphql import GraphQLError
import SessionManager

from schema import schema

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "aaaaaaaaaa"  # change this!
app.config["REFRESH_EXP_LENGTH"] = 30
app.config["ACCESS_EXP_LENGTH"] = 10

auth = GraphQLAuth(app)

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(debug=True)
