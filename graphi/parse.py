""" API for parsing GraphQL statements """

import re
from graphi.schema import GraphQLType, Field
from graphi.query import GraphQLContext, GraphQLBlock
from typing import List, Iterator


class GraphQLParser:
    def __init__(self, ctx: GraphQLContext):
        self.context = ctx
    
    def parse(self, s: str) -> Iterator[GraphQLBlock]:
        """ Parses a GraphQL expression string, yielding GraphQLBlock objects """
        query_stack = []
        for j, char in enumerate(s):
            if char == "{":
                query_stack.append(j)
            elif char == "}":
                i = query_stack.pop()
                substr = s[i + 1 : j]
                lines = substr.split("\n")
                yield from self._parse_block_lines(lines)

    def _parse_block_lines(self, lines: List[str]) -> Iterator[GraphQLBlock]:
        blocks = []
        attrs = []
        for line in lines:
            line = self._remove_comment(line)

            # RegEx matching
            match_start_of_block = self._match_start_of_block(line)
            match_end_of_block = self._match_end_of_block(line)
            match_block_attr = self._block_attr(line)

            if match_start_of_block:
                block_name, block_args = match_start_of_block.groups()
                new_block = GraphQLBlock()
                blocks.append(new_block)
            elif match_end_of_block:
                next_block = blocks.pop()
                next_block.attrs = attrs
                yield next_block
                attrs = [next_block]
            elif line:
                attrs.append(line.strip())  # TODO: should do a regex for single word
            # TODO: write regex to detect:
            # - arguments
            # - nested query on object
            # - fragments

    def _match_start_of_block(self, line: str):
        """ Use RegEx to match the start of GraphQL block """
        return re.match(r"^(?:query\s)?(\w+)?(?(1)(\(.+\))?|)\s?{", line.strip())
    
    def _match_end_of_block(self, line: str):
        return line.endswith("}")
    
    def _match_block_attr(self, line: str):
        return line

    def _remove_comment(self, line: str) -> str:
        if "#" in line:
            return line.partition("#")[0].strip()
        return line.strip()
