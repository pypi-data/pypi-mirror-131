from typing import Literal, Union
from termcolor import colored


# Expression Errors
class SyntaxError(Exception):
    pass


class TokenizationError(SyntaxError):
    def __init__(self,
                 expression_simplified: str,
                 kind: Union[Literal['symbol'], Literal['token']],
                 i: int,
                 j: int,
                 *args: object) -> None:
        super().__init__('Unknown {} {} encountered in {}{}{}'.format(
            kind,
            expression_simplified[i:j],
            colored(text=expression_simplified[:i], color='green'),
            colored(text=expression_simplified[i:j], color='red'),
            expression_simplified[j:]
        ), *args)


class LexingError(SyntaxError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ParsingError(SyntaxError):
    pass


# Tree Errors
class TreeError(Exception):
    pass


class RegistrationError(Exception):
    pass


class BuildTreeError(TreeError):
    pass


class UpdateTreeError(TreeError):
    pass


class ReduceTreeError(TreeError):
    pass


class TreeReprError(TreeError):
    pass
