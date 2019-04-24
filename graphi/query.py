""" API for parsing and evaluating GraphQL queries"""

import sqlite3
from typing import List, Dict
from graphi.parse import GraphQLParser
from graphi.schema import GraphQLType


class GraphQLQuery:
    def __init__(self):
        pass


class GraphQLContext:
    def __init__(self, types: List[GraphQLType], conn: sqlite3.Connection = None):
        self.types = {t.name: t for t in types}
        self.parser = GraphQLParser(self)
        if conn:
            cursor = conn.cursor()
            cursor.execute(self.create_tables())
            conn.commit()
        self.conn = conn

    def create_tables(self):
        """ Performs SQL table setup for each defined GraphQL type """
        map_sql_types = {str: "TEXT", int: "INTEGER"}
        statements = []
        for t in self.types.values():
            fields = ["id INTEGER PRIMARY KEY"]
            for field in t.fields:
                if field.fieldtype in map_sql_types:
                    fields.append(f"{field.name} {map_sql_types[field.fieldtype]}")
                    # TODO: nullable?
                else:
                    # TODO: foreign key
                    fields.append(f"{field.name} INTEGER")
                    fields.append(
                        f"FOREIGN KEY({field.name}) REFERENCES {field.blocktype.name}(id)"
                    )
            fields_string = ",\n".join(fields)
            statements.append(
                f"CREATE TABLE IF NOT EXISTS {t.name} (\n{fields_string}\n);"
            )
        return "\n".join(statements)

    def execute(self, graphql_str: str):
        """ Executes GraphQL input """
        block = self.parser.parse(graphql_str)
        sql_command = block.to_sql()
        cursor = self.conn.cursor()
        result = cursor.execute(sql_command)
        return result
