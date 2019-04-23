import pytest
from graphi.schema import GraphQLType, Field, Argument
from graphi.query import GraphQLContext, GraphQLQuery, GraphQLBlock
from graphi.parse import GraphQLParser


@pytest.fixture
def setup_person_query():
    name = Field("name", fieldtype=str, nullable=False)
    age = Field("age", fieldtype=int, nullable=False)
    person = GraphQLType([name, age], name="person")
    ctx = GraphQLContext([person])
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
