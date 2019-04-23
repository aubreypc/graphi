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
