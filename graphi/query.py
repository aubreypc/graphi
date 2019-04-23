""" API for parsing and evaluating GraphQL queries"""

from typing import List
from graphi.schema import GraphQLType


class GraphQLQuery:
    def __init__(self):
        pass


class GraphQLContext:
    def __init__(self, types: List[GraphQLType]):
        self.types = types


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


class GraphQLExpression:
    def __init__(self):
        pass
