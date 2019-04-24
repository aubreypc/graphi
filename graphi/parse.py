""" API for parsing GraphQL statements """

import re
from graphi.schema import GraphQLType, Field
from graphi.block import GraphQLBlock
from typing import List, Iterator, Dict


class GraphQLParser:
    def __init__(self, context):
        self.context = context

    def parse(self, s: str):
        blocks = []
        for line in s.split("\n"):
            line = self._remove_comment(line)
            if not line:
                continue

            # RegEx matching
            match_start_of_block = self._match_start_of_block(line)
            match_end_of_block = self._match_end_of_block(line)
            match_block_attr = self._match_block_attr(line)
            match_fragment = self._match_fragment(line)

            if match_start_of_block:
                operation, block_name, block_args = match_start_of_block.groups()
                if block_name:
                    if block_name in self.context.types:
                        inferred_blocktype = self.context.types[block_name]
                    else:
                        inferred_blocktype = GraphQLType(name=block_name)
                else:
                    inferred_blocktype = None
                if block_args:
                    block_args = self._parse_arguments(block_args)
                new_block = GraphQLBlock(
                    blocktype=inferred_blocktype, operation=operation, args=block_args
                )
                blocks.append(new_block)
            elif match_end_of_block:
                next_block = blocks.pop()
                if blocks:
                    blocks[-1].children.append(next_block)
                else:
                    return next_block
            elif match_block_attr:
                if blocks:
                    blocks[-1].attrs.append(line)
            elif match_fragment:
                # TODO: handle fragments
                pass
            else:
                raise Exception(f"Could not parse {line}")

    def _match_start_of_block(self, line: str):
        """ Use RegEx to match the start of GraphQL block """
        return re.match(
            r"^(query\s|mutation\s)?(\w+)?(?(2)(\(.+\))?|)\s?{", line.strip()
        )

    def _match_end_of_block(self, line: str):
        return line.endswith("}")

    def _match_block_attr(self, line: str):
        return re.match(r"^\b\w+\b$", line)

    def _match_fragment(self, line: str):
        return re.match(r"^...\b\w+\b$", line)

    def _remove_comment(self, line: str) -> str:
        if "#" in line:
            return line.partition("#")[0].strip()
        return line.strip()

    def _parse_arguments(self, arguments: str) -> Dict:
        arguments = arguments[1:-1]  # Strip parentheses
        arguments = arguments.split(",")
        parsed_args = {}
        for argpair in arguments:
            assert ":" in argpair
            key, _, val = argpair.partition(":")
            key, val = key.strip(), val.strip()
            parsed_args[key] = val
        return parsed_args
