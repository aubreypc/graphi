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
    def __init__(self, attrs: List[str] = None, blocktype: GraphQLType = None):
        self.attrs = [] if attrs is None else attrs
        self.blocktype = blocktype

class GraphQLExpression:
    def __init__(self):
        pass
