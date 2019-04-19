""" Objects for working with GraphQL schemas """

from typing import List, Dict, Callable
from inspect import signature, _empty
from .exceptions import MethodNotImplemented, NullField


class Argument:
    def __init__(self, name, argtype, default=None):
        self.name = name
        self.type = argtype
        self.default = default


class Field:
    def __init__(
        self,
        name: str,
        fieldtype=None,
        func: Callable = None,
        args: List[Argument] = None,
        returntype=None,
        nullable: bool = True,
    ):
        self.name = name
        self.nullable = nullable
        self.fieldtype = fieldtype
        self.func = func
        if func and func.__annotations__:
            # Infer the arguments and return type from func's type annotations
            self.args = []
            self.returntype = func.__annotations__["return"]
            func_sig = signature(func)
            for argname, argtype in func.__annotations__.items():
                if argname == "return":
                    continue
                default = func_sig.parameters[argname].default
                if isinstance(default, _empty):  # Function signature has no default val
                    default = None
                arg = Argument(argname, argtype, default=default)
                self.args.append(arg)
        else:
            self.args = args
            self.returntype = returntype

    def is_function(self):
        return self.args != [] and self.returntype is not None

    def validate(self, value):
        if self.is_function():
            if self.func is None:
                raise MethodNotImplemented(f"Function {self.name} is not implemented")
            elif not isinstance(value, dict):
                raise TypeError(
                    f"Argument to Field.validate must be a dict of arguments when field is a function"
                )
        elif not isinstance(value, self.fieldtype):
            raise TypeError(
                f"Received {type(value)} for field {self.name}; {self.fieldtype} expected"
            )
        return True


class GraphQLType:
    def __init__(self, fields: List[Field]):
        self.fields = fields

    def validate(self, data: Dict):
        for field in self.fields:
            if field.name not in data and not field.nullable:
                raise NullField(f"{field.name} is a required field")
            field.validate(data[field.name])
        return True
