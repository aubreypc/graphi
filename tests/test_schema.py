""" Tests for the GraphQL schema Python API """

import pytest
from graphi.schema import GraphQLType, Field, Argument
from graphi.exceptions import MethodNotImplemented


def test_field_infer_function():
    """ Field object should infer arguments, default values, and return types from type annotations """

    def my_func(name: str = "Simone", num: int = 1) -> str:
        return f"{name} is #{num}!"

    my_field = Field("my_field", func=my_func)
    assert my_field.is_function()
    assert my_field.args[0].type is str
    assert my_field.args[0].default == "Simone"
    assert my_field.args[1].type is int
    assert my_field.args[1].default == 1


def test_field_validate_typeerror():
    """ Field object should raise a TypeError when validating with wrong type """
    with pytest.raises(TypeError) as exc_info:
        my_field = Field("my_field", fieldtype=int)
        assert not my_field.validate("not an int")


def test_field_validate_function_not_implemented():
    """ Field object should raise an exception when validating an undefined function """
    with pytest.raises(MethodNotImplemented) as exc_info:
        args = (Argument("name", str), Argument("num", int))
        my_field = Field("my_field", args=args, returntype=str)
        assert not my_field.validate({"name": "Simone", "num": 1})
