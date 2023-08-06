from typing import Callable, List, Literal, Union

from .operand_ import Operand
from .exceptions import ReduceTreeError
from .node import Node


class Operator(Node):
    def __init__(self,
                 symbol: str,
                 func: Callable,
                 priority: int,
                 kind: Union[Literal['pre'], Literal['in'],
                             Literal['post']] = 'in',
                 operands: int = 2,
                 **kwargs):
        super().__init__(**kwargs)
        self.symbol: str = symbol
        self.priority = priority
        self.kind = kind
        self.operands = operands
        self.func = func
        self.width = len(symbol)

    def __call__(self) -> Union[int, float]:
        if self.children is None:
            raise ReduceTreeError('Tree is not complete')
        return self.func(*map(lambda op: op.value, self.children))

    def __str__(self):
        return f'{self.symbol:^{self.width}}'

    def __repr__(self) -> str:
        return f'Operator({self.symbol}, kind=\'{self.kind}\', operands={self.operands})'

    def isFull(self) -> bool:
        return len(self.children) == self.operands

    def __lt__(self, otherNode) -> bool:
        if isinstance(otherNode, Operator):
            return self.priority < otherNode.priority
        elif isinstance(otherNode, Operand):
            return True
        raise

    def __le__(self, otherNode) -> bool:
        if isinstance(otherNode, Operator):
            return self.priority <= otherNode.priority
        elif isinstance(otherNode, Operand):
            return True
        raise

    def __gt__(self, otherNode) -> bool:
        if isinstance(otherNode, Operator):
            return self.priority > otherNode.priority
        elif isinstance(otherNode, Operand):
            return False
        raise

    def __ge__(self, otherNode) -> bool:
        if isinstance(otherNode, Operator):
            return self.priority >= otherNode.priority
        elif isinstance(otherNode, Operand):
            return False
        raise
