from graphi.schema import GraphQLType
from typing import List, Dict


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
                    # Correct child's inferred block type if it refers to parent's field
                    parent_field = self.blocktype.field(child.blocktype.name)
                    if parent_field:
                        child.blocktype = parent_field.fieldtype
                    child_query = child.to_sql()[0:-1]  # Strip the semicolon
                    child_queries.append(f"({child_query})")
                nested = ", " + ", ".join(child_queries)
            if self.args:
                args = [f"{arg}={val}" for arg, val in self.args.items()]
                args_string = ", ".join(args)
                where = f" WHERE {args_string}"
            return f"SELECT {attrs_string}{nested} FROM {self.blocktype.name}{where};"
