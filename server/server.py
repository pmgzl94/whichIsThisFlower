import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(name = graphene.String(default_value="World"))

    def resolve_hello(self, info, name):
        return "Hello " + name

schema = graphene.Schema(query=Query)

# result = schema.execute('{ hello }')
# print (result.data["hello"])


from flask import Flask
from flask_graphql import GraphQLView

# from schema import schema

app = Flask(__name__)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))



# Optional, for adding batch query support (used in Apollo-Client)
# app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view(
#     'graphql',
#     schema=schema,
#     batch=True
# ))

if __name__ == '__main__':
    app.run()