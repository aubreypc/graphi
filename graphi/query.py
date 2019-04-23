""" API for parsing and evaluating GraphQL queries"""

from typing import List
from graphi.schema import GraphQLType


class GraphQLQuery:
    def __init__(self):
        pass


class GraphQLBlock:
    def __init__(
        self,
        attrs: List[str] = None,
        children: List[GraphQLType] = None,
        blocktype: GraphQLType = None,
        operation=None,
    ):
        self.attrs = [] if attrs is None else attrs
        self.children = [] if children is None else children
        self.blocktype = blocktype
        self.operation = operation


class GraphQLContext:
    def __init__(self, types: List[GraphQLType]):
        self.types = {t.name: t for t in types}

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
                    pass
            fields_string = ",\n".join(fields)
            statements.append(
                f"CREATE TABLE IF NOT EXISTS {t.name} (\n{fields_string}\n);"
            )
        return "\n".join(statements)

    def resolve(self, block: GraphQLBlock):
        """ Attempts to execute a query or mutation """
        pass
