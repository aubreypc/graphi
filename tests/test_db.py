""" Tests for executing database commands """

import pytest


def test_create_tables(setup_person_query):
    ctx, block = setup_person_query()
    expected = """\
CREATE TABLE IF NOT EXISTS person (
id INTEGER PRIMARY KEY,
name TEXT,
age INTEGER
);"""
    assert ctx.create_tables() == expected
    # TODO: assert schema is as it should be


def test_block_to_sql(setup_person_query):
    ctx, block = setup_person_query()
    query1 = block.children[0]
    expected1 = "SELECT name, age FROM person WHERE id=1;"
    assert query1.to_sql() == expected1

    query2 = block.children[1]
    expected2 = "SELECT age FROM person WHERE id=2;"
    assert query2.to_sql() == expected2

    assert block.to_sql() == f"{expected1}\n{expected2}"


@pytest.mark.skip(reason="Deprecated")
def test_nested_block_to_sql(setup_person_pet_query):
    ctx, block = setup_person_pet_query()
    expected = "SELECT name, species, (SELECT name, age FROM person WHERE id=pet.owner) FROM pet WHERE id=1;"
    assert block.to_sql() == expected


def test_resolve_block(setup_person_pet_query):
    ctx, block = setup_person_pet_query()
    expected = {
        "data": {
            "name": "Annabelle",
            "species": "cat",
            "owner": {"name": "Aubrey", "age": 21},
        }
    }
    assert block.resolve(ctx.conn) == expected
