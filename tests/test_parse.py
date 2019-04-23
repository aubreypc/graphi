""" Tests for GraphQL language parsing """

import pytest
from graphi.schema import GraphQLType, Field, Argument
from graphi.query import GraphQLContext, GraphQLQuery, GraphQLBlock
from graphi.parse import GraphQLParser


def test_remove_comment():
    parser = GraphQLParser(None)
    uncommented = "before the comment"
    comment = "this is a comment. comments are #1"
    assert parser._remove_comment(f"{uncommented} #{comment}") == uncommented


def test_match_end_of_block():
    parser = GraphQLParser(None)
    assert parser._match_end_of_block("}")
    assert not parser._match_end_of_block("")
    assert not parser._match_end_of_block("attr")


def test_match_start_of_block():
    parser = GraphQLParser(None)
    assert parser._match_start_of_block("{")
    assert parser._match_start_of_block("obj {")
    assert parser._match_start_of_block("query obj(arg1: $arg1) {")
    assert not parser._match_start_of_block("")


def test_parse_block():
    name = Field("name", fieldtype=str, nullable=False)
    age = Field("age", fieldtype=int, nullable=False)
    person = GraphQLType([name, age])
    ctx = GraphQLContext([person])
    parser = GraphQLParser(ctx)

    blocks = parser.parse(
        """
    {
        person(id: 1){
            name
            age
        }

        person(id: 2) {
            age
        }
    }
    """
    )
    blocks = [block for block in blocks]
    print([(block, block.blocktype.name, block.attrs) for block in blocks])
    assert isinstance(blocks[0], GraphQLBlock)
    assert blocks[0].blocktype.name == "person"
    assert blocks[0].attrs[0] == "name"
    assert blocks[0].attrs[1] == "age"
    assert blocks[1].attrs[0] == "age"
