""" Objects for working with GraphQL schemas """

from typing import List, Dict, Callable
from .exceptions import MethodNotImplemented


class Argument:
    def __init__(self, name, argtype, default=None):
        self.name = name
        self.type = argtype
        self.default = default
        self.required = default is None


class Field:
    def __init__(
        self,
        name: str,
        field_type=None,
        func: Callable = None,
        args: List[Argument] = None,
        returntype=None,
        nullable: bool = True,
    ):
        self.name = name
        self.nullable = nullable
        self.field_type = field_type
        self.func = func
        if func and func.__annotations__:
            # Infer the arguments and return type from func's type annotations
            self.args = []
            self.returntype = func.__annotations__["return"]
            for argname, argtype in func.__annotations__.items():
                if argname == "return":
                    continue
                # TODO: pass default value to Argument
                arg = Argument(argname, argtype)
                self.args.append(arg)
        else:
            self.args = args
            self.returntype = returntype

    def is_function(self):
        return self.args != [] and self.returntype is not None

    def validate(self, data):
        if self.is_function() and self.func is None:
            raise MethodNotImplemented(f"Function {self.name} is not implemented")
        return True


class GraphQLType:
    def __init__(self, fields: List[Field]):
        self.fields = fields

    def validate(self, data: Dict):
        for field in self.fields:
            if field.name not in data and not field.nullable:
                raise Exception(f"{field.name} is a required field")
