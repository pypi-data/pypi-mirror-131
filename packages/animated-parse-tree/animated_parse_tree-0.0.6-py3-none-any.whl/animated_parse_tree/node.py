from abc import abstractmethod
from typing import Any, List, Optional


class Node:
    def __init__(self,
                 value=None):
        self.parent: Optional[Node] = None
        self.children: List[Node] = []
        self.value: Any = value
        self.height: int = 1
        self.width: int = 0

    @abstractmethod
    def isFull(self) -> bool:
        pass

    @abstractmethod
    def isEmpty(self) -> bool:
        pass

    @abstractmethod
    def __lt__(self, otherNode) -> bool:
        pass

    @abstractmethod
    def __le__(self, otherNode) -> bool:
        pass

    @abstractmethod
    def __gt__(self, otherNode) -> bool:
        pass

    @abstractmethod
    def __ge__(self, otherNode) -> bool:
        pass

    def __call__(self) -> Any:
        return self.value

    @abstractmethod
    def __str__(self) -> str:
        pass