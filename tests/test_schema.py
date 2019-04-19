""" Tests for the GraphQL schema Python API """

import pytest
from graphi.schema import GraphQLType, Field, Argument
from graphi.exceptions import MethodNotImplemented


def test_field_infer_function_type():
    """ Field object should infer arguments and return types from type annotations """

    def my_func(name: str, num: int) -> str:
        return f"{name} is #{num}!"

    my_field = Field("my_field", func=my_func)
    assert my_field.is_function()
    assert my_field.args
    assert my_field.args[0].type is str
    assert my_field.args[1].type is int


def test_validate_function_not_implemented():
    """ Field object should raise an exception when validating an undefined function """
    with pytest.raises(MethodNotImplemented) as exc_info:
        args = (Argument("name", str), Argument("num", int))
        my_field = Field("my_field", args=args, returntype=str)
        my_field.validate({"name": "Simone", "num": 1})
