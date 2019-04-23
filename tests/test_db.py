""" Tests for executing database commands """

import pytest


@pytest.mark.skip(reason="WIP")
def test_resolve(setup_person_query):
    ctx, block = setup_person_query()
    assert ctx.resolve(block) is True


def test_create_tables(setup_person_query):
    ctx, block = setup_person_query()
    expected = """\
CREATE TABLE IF NOT EXISTS person (
id INTEGER PRIMARY KEY,
name TEXT,
age INTEGER
);"""
    assert ctx.create_tables() == expected


def test_block_to_sql(setup_person_query):
    ctx, block = setup_person_query()
    query1 = block.children[0]
    expected = "SELECT name, age FROM person WHERE id=1;"
    # TODO: to get passing, need to implement argument parsing so query1.args == {"id": 1}
    assert query1.to_sql() == expected
