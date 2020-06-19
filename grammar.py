import re
import yaml
from typing import Dict, List, Union, Optional, Callable, Tuple

_predefined_leaves = {
    'WHITESPACE': r'\s*',
    'ALPHA': r'[a-Z]+'
}


class SubExpression:
    def __init__(self, key: str, expr: str):
        self.key = key
        self.expr = expr


class Token:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class PartialMatch:
    def __init__(self, input_str: str):
        self.input_str = input_str
        self.parts: List[Union[Token, SubExpression]] = {}

    def is_full(self) -> bool:
        return all(map(lambda part: isinstance(part, Token), self.parts))


class Node:
    def __init__(self, expr: str, leaves: Dict[str, str]):
        parts: List[str] = re.split(r'\s+', expr)
        pattern = "^"
        groupies: List[Callable[[PartialMatch, str], None]] = []
        for part in parts:
            leaf = leaves[part]
            if leaf:
                groupies.append(
                    lambda match, group: match.parts.append(Token(part, group)))
                pattern += f"({leaf})"
            else:
                groupies.append(lambda match, group: match.parts.append(
                    SubExpression(part, group)))
                pattern += r"([^\s]+)"
        self.match_applicators = groupies
        pattern += "$"
        self.regex = re.compile(pattern)
        self.child_keys: List[str]

    def match(self, input_str: str) -> Optional[PartialMatch]:
        match = self.regex.match(input_str)
        match_applicators = self.match_applicators
        result = PartialMatch(input_str)
        if match:
            for index, group in enumerate(match.groups()):
                match_applicators[index](result, group)
        else:
            return None
        return result


class Grammar:
    def __init__(self, grammar_file):
        self.leaves: Dict[str, str] = {}
        self.raw_nodes: Dict[str, Union[List[str], str]] = {}
        with open(grammar_file) as f:
            raw = yaml.load(f, Loader=yaml.Loader)
        for key, value in raw.items():
            if key.isupper():
                self.leaves[key] = value
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


if __name__ == "__main__":
    grammar = Grammar('expression.yaml')
