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
    expected1 = "SELECT name, age FROM person WHERE id=1;"
    assert query1.to_sql() == expected1

    query2 = block.children[1]
    expected2 = "SELECT age FROM person WHERE id=2;"
    assert query2.to_sql() == expected2

    assert block.to_sql() == f"{expected1}\n{expected2}"


def test_nested_block_to_sql(setup_person_pet_query):
    ctx, block = setup_person_pet_query()
    expected = "SELECT name, species, (SELECT name, age FROM person WHERE id=pet.owner) FROM pet WHERE id=1;"
    assert block.to_sql() == expected
