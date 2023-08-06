from .node import Node


class Temp_Node(Node):
    def __init__(self,
                 parent: Node,
                 blank: str = ' '):
        super().__init__()
        self.parent = parent
        self.width = parent.width
        self.blank: str = blank
        parent.children.append(self)

    def __str__(self):
        return self.blank * self.width

    def __repr__(self) -> str:
        return f'TempNode(width={self.width})'