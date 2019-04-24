""" Tests for GraphQL language parsing """

import pytest
from graphi.schema import GraphQLType, Field, Argument
from graphi.query import GraphQLContext, GraphQLQuery
from graphi.block import GraphQLBlock
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


def test_parse_block(setup_person_query):
    ctx, block = setup_person_query()
    assert isinstance(block, GraphQLBlock)
    assert block.blocktype is None
    assert len(block.attrs) == 0
    assert len(block.children) == 2

    person_1 = block.children[0]
    assert person_1.blocktype.name == "person"
    assert person_1.attrs[0] == "name"
    assert person_1.attrs[1] == "age"

    person_2 = block.children[1]
    assert person_2.blocktype.name == "person"
    assert person_2.attrs[0] == "age"
