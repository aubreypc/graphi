import sqlite3
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
            # Outermost block of query: return all child queries
            return "\n".join([child.to_sql() for child in self.children])
        if self.attrs:
            where = ""
            select_string = ", ".join(
                self.attrs + [child.blocktype.name for child in self.children]
            )
            if self.args:
                args = [f"{arg}={val}" for arg, val in self.args.items()]
                args_string = ", ".join(args)
                where = f" WHERE {args_string}"
            return f"SELECT {select_string} FROM {self.blocktype.name}{where};"

    def resolve(self, conn: sqlite3.Connection, is_root=True):
        if is_root and not self.attrs:
            # Outermost block of query: return all child queries
            if len(self.children) > 1:
                return {
                    "data": [
                        child.resolve(conn, is_root=False) for child in self.children
                    ]
                }
            return {"data": self.children[0].resolve(conn, is_root=False)}
        elif not self.children and not self.attrs:
            # No attrs or foreign keys; no need to query
            return {}
        cursor = conn.cursor()
        sql_cmd = self.to_sql()
        query = cursor.execute(sql_cmd)
        query_description = [t[0] for t in query.description]
        # TODO: could be multiple result if many-to-one; can't just fetchone()
        query_data = {
            attr: val for attr, val in zip(query_description, query.fetchone())
        }
        data = {attr: query_data[attr] for attr in self.attrs}
        for child in self.children:
            # Use parent's foreign key to locate child by id
            child.args["id"] = query_data[child.blocktype.name]
            # Correct child's inferred block type if it refers to parent's field
            queried_field_name = child.blocktype.name
            parent_field = self.blocktype.field(queried_field_name)
            if parent_field:
                child.blocktype = parent_field.fieldtype
            resolved = child.resolve(conn, is_root=False)
            data[queried_field_name] = child.resolve(conn, is_root=False)
        if is_root:
            return {"data": data}
        return data
