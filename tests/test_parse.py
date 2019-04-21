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


@pytest.mark.skip(reason="dev")
def test_parse_block():
    name = Field("name", fieldtype=str, nullable=False)
    age = Field("age", fieldtype=int, nullable=False)
    person = GraphQLType([name, age])
    ctx = GraphQLContext([person])
    parser = GraphQLParser(ctx)

    blocks = parser.parse("""
    {
        person(id: 1){
            name
            age
        }
    }
    """)
    blocks = [block for block in blocks]
    assert isinstance(blocks[0], GraphQLBlock)
    assert blocks[0].blocktype.name == "person"
