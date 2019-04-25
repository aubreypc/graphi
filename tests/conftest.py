import pytest
import sqlite3 as sqlite
from graphi.schema import GraphQLType, Field, Argument
from graphi.query import GraphQLContext, GraphQLQuery
from graphi.block import GraphQLBlock
from graphi.parse import GraphQLParser


@pytest.fixture(scope="function")
def setup_person_query(tmp_path):
    conn = sqlite.connect(str(tmp_path / "data.db"))
    name = Field("name", fieldtype=str, nullable=False)
    age = Field("age", fieldtype=int, nullable=False)
    person = GraphQLType([name, age], name="person")
    ctx = GraphQLContext([person], conn=conn)
    parser = GraphQLParser(ctx)

    def _setup_fn(*args):
        if args:
            return ctx, parser.parse(args[0])
        else:
            return (
                ctx,
                parser.parse(
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
                ),
            )

    return _setup_fn


@pytest.fixture(scope="function")
def setup_person_pet_query(tmp_path):
    conn = sqlite.connect(str(tmp_path / "data.db"))
    person_name = Field("name", fieldtype=str, nullable=False)
    person_age = Field("age", fieldtype=int, nullable=False)
    person = GraphQLType([person_name, person_age], name="person")

    pet_name = Field("name", fieldtype=str, nullable=False)
    pet_species = Field("species", fieldtype=str, nullable=False)
    pet_owner = Field("owner", fieldtype=person, nullable=False)
    pet = GraphQLType([pet_name, pet_species, pet_owner], name="pet")

    ctx = GraphQLContext([person, pet], conn=conn)
    parser = GraphQLParser(ctx)

    cursor = conn.cursor()
    cursor.execute("INSERT INTO person VALUES (1, 'Aubrey', 21);")
    cursor.execute("INSERT INTO pet VALUES (1, 'Annabelle', 'cat', 1);")
    conn.commit()

    def _setup_fn(*args):
        if args:
            return ctx, parser.parse(args[0])
        else:
            return (
                ctx,
                parser.parse(
                    """
    {
        pet(id: 1){
            name
            species
            owner {
                name
                age
            }
        }
    }
    """
                ),
            )

    return _setup_fn
