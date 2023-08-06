from typing import Optional, Union
from .node import Node


class Operand(Node):
    def __init__(self,
                 value: Union[int, float],
                 symbol: Optional[str]=None,
                 **kwargs):
        super().__init__(value=value, **kwargs)
        self.symbol: str = str(value) if symbol is None else symbol
        self.width = len(self.symbol)

    def __str__(self):
        return f'{self.symbol:^{self.width}}'

    def __repr__(self) -> str:
        return f'Operand({self.value})'

    def isFull(self) -> bool:
        return True

    def __lt__(self, otherNode) -> bool:
        return False

    def __le__(self, otherNode) -> bool:
        return False

    def __gt__(self, otherNode) -> bool:
        return True

    def __ge__(self, otherNode) -> bool:
        return True