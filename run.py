import sqlite3
import json
from flask import Flask, request
from graphi.schema import GraphQLType, Field
from graphi.query import GraphQLContext


app = Flask(__name__)
conn = sqlite3.connect("data.db")

# Define GraphQL types
person_name = Field("name", fieldtype=str, nullable=False)
person_age = Field("age", fieldtype=int, nullable=False)
person = GraphQLType([person_name, person_age], name="person")
pet_name = Field("name", fieldtype=str, nullable=False)
pet_species = Field("species", fieldtype=str, nullable=False)
pet_owner = Field("owner", fieldtype=person, nullable=False)
pet = GraphQLType([pet_name, pet_species, pet_owner], name="pet")

graphql = GraphQLContext([person, pet], conn=conn)


@app.route("/", methods=["POST"])
def execute_graphql_command():
    conn = sqlite3.connect("data.db")
    command = request.data.decode()
    result = graphql.execute(conn, command)
    return json.dumps(result)


if __name__ == "__main__":
    app.run(debug=True)
