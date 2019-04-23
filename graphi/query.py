""" API for parsing and evaluating GraphQL queries"""

from typing import List, Dict
from graphi.schema import GraphQLType


class GraphQLQuery:
    def __init__(self):
        pass


class GraphQLBlock:
    def __init__(
        self,
        attrs: List[str] = None,
        args: Dict = None,
        children: List[GraphQLType] = None,
        blocktype: GraphQLType = None,
        operation=None,
    ):
        self.attrs = [] if attrs is None else attrs
        self.args = {} if args is None else args
        self.children = [] if children is None else children
        self.blocktype = blocktype
        self.operation = operation

    def to_sql(self):
        if self.children and not self.blocktype:
            # Outermost block of query: return sum of child queries
            return "\n".join([child.to_sql() for child in self.children])
        if self.attrs:
            attrs_string = ", ".join([attr for attr in self.attrs])
            where = ""
            nested = ""
            if self.children:
                child_queries = []
                for child in self.children:
                    child.args["id"] = f"{self.blocktype.name}.{child.blocktype.name}"
                    # TODO: child's inferred blocktype is wrong
                    # TODO: need to look up correct blocktype via schema?
                    nested_query_on_attr = self.blocktype.field(child.blocktype.name)
                    if nested_query_on_attr:
                        child.blocktype = nested_query_on_attr.fieldtype
                    child_query = child.to_sql()[0:-1]  # Strip the semicolon
                    child_queries.append(f"({child_query})")
                nested = ", " + ", ".join(child_queries)
            if self.args:
                args = [f"{arg}={val}" for arg, val in self.args.items()]
                args_string = ", ".join(args)
                where = f" WHERE {args_string}"
            return f"SELECT {attrs_string}{nested} FROM {self.blocktype.name}{where};"


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
                    fields.append(f"{field.name} INTEGER")
                    fields.append(
                        f"FOREIGN KEY({field.name}) REFERENCES {field.blocktype.name}(id)"
                    )
            fields_string = ",\n".join(fields)
            statements.append(
                f"CREATE TABLE IF NOT EXISTS {t.name} (\n{fields_string}\n);"
            )
        return "\n".join(statements)

    def resolve(self, block: GraphQLBlock):
        """ Attempts to execute a query or mutation """
        pass
