import json
import re
import yaml
from typing import Dict, List, Union, Optional, Callable, Tuple

_predefined_leaves = {
    'WHITESPACE': r' ',
    'ALPHA': r'[A-Za-z]+',
    'NUMERIC': r'\d+'
}


class SubExpression:
    def __init__(self, key: str, expr: str):
        self.key = key
        self.expr = expr

    def __str__(self):
        return f"{self.key}->{self.expr}"

    def __repr__(self):
        return self.__str__()


class Token:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name}=\"{self.value}\""

    def __repr__(self):
        return self.__str__()


class PartialMatch:
    def __init__(self, key: str, input_str: str):
        self.key = key
        self.input_str = input_str
        self.parts: List[Union[Token, SubExpression, PartialMatch]] = []

    def is_full(self) -> bool:
        return not any(map(lambda part: isinstance(part, SubExpression), self.parts))

    def __str__(self):
        return str({
            "key": self.key,
            "parts": self.parts
        })

    def __repr__(self):
        return self.__str__()


class Node:
    def __init__(self, expr: str, leaves: Dict[str, str]):
        self.expr = expr
        parts: List[str] = re.split(r'\s+', expr)
        pattern = "^"
        groupies: List[Callable[[PartialMatch, str], None]] = []
        for part in parts:
            try:
                leaf = leaves[part]
                groupies.append(Node._leaf_match(part))
                pattern += f"({leaf})"
            except KeyError:
                groupies.append(Node._node_match(part))
                pattern += r"(.+)"
        self.match_applicators = groupies
        pattern += "$"
        self.pattern = pattern
        self.regex = re.compile(pattern)
        self.child_keys: List[str]

    @staticmethod
    def _leaf_match(part: str):
        def apply(match, group):
            match.parts.append(Token(part, group))
        return apply

    @staticmethod
    def _node_match(part: str):
        def apply(match, group):
            match.parts.append(SubExpression(part, group))
        return apply

    def match(self, key: str, input_str: str) -> Optional[PartialMatch]:
        match = self.regex.match(input_str)
        match_applicators = self.match_applicators
        result = PartialMatch(key, input_str)
        if match:
            for index, group in enumerate(match.groups()):
                match_applicators[index](result, group)
        else:
            return None
        return result

    def __str__(self):
        return self.expr


class Grammar:
    def __init__(self, grammar_file):
        self.leaves: Dict[str, str] = {}
        self.raw_nodes: Dict[str, Union[List[str], str]] = {}
        with open(grammar_file) as f:
            raw = yaml.load(f, Loader=yaml.Loader)
        for key, value in raw.items():
            if key.isupper():
                self.leaves[key] = re.escape(value)
            else:
                self.raw_nodes[key] = value

        self.leaves.update(_predefined_leaves)

        self.nodes: Dict[str, List[Node]] = {key: Grammar._create_nodes(value, self.leaves)
                                             for key, value in self.raw_nodes.items()}

    @staticmethod
    def _create_nodes(value: Union[str, List[str]], leaves: Dict[str, str]) -> List[Node]:
        if isinstance(value, str):
            return [Node(value, leaves)]
        else:
            return [Node(expr, leaves) for expr in value]

    def _parse(self, partial_match: PartialMatch) -> Optional[PartialMatch]:
        new_match = PartialMatch(partial_match.key, partial_match.input_str)
        for part in partial_match.parts:
            if isinstance(part, Token):
                new_match.parts.append(part)
            elif isinstance(part, PartialMatch):
                new_match.parts.append(part)
            else:
                resolved: List[Node] = self.nodes[part.key]
                match = None
                for node in resolved:
                    sub_match = node.match(part.key, part.expr)
                    if sub_match:
                        parsed_sub_match = self._parse(sub_match)
                        if parsed_sub_match:
                            match = parsed_sub_match
                            break
                if match:
                    new_match.parts.append(match)
                else:
                    return None
        return new_match

    def parse(self, expr: str) -> PartialMatch:
        start = SubExpression('root', expr)
        match = PartialMatch('<root>', expr)
        match.parts.append(start)
        while(match and not match.is_full()):
            match = self._parse(match)
        return match


if __name__ == "__main__":
    grammar = Grammar('expression.yaml')
    match = grammar.parse("int: var + 1")
    if match:
        print(match)
    else:
        print("No match")
