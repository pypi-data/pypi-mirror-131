from typing import List, Literal, Optional, Union, cast

from .exceptions import TreeReprError, UpdateTreeError
from .temp_node import Temp_Node
from .node import Node


class Tree:
    def __init__(self,
                 root: Node = None,
                 padding: int = 1,
                 left_branch: str = '/',
                 middle_branch: str = '|',
                 right_branch: str = '\\'):
        self.root: Optional[Node] = root
        self.currentPointer: Optional[Node] = None
        self.left_branch: str = left_branch
        self.middle_branch: str = middle_branch
        self.right_branch: str = right_branch
        self.padding: int = padding

    def insert(self, node: Node):
        if self.root is None or self.currentPointer is None:
            self.root = self.currentPointer = node
        elif not self.currentPointer.isFull():
            node.parent = self.currentPointer
            self.currentPointer.children.append(node)
        else:
            if node > self.currentPointer:
                node.children.append(self.currentPointer.children.pop())
                self.currentPointer.children.append(node)
                self.currentPointer = node
            else:
                self.float_node(node=node)

    def float_node(self, node: Node):
        if self.currentPointer is None:
            self.root.parent = node
            node.children.append(self.root)
            self.root = node
            self.currentPointer = self.root
        elif node <= self.currentPointer:
            self.currentPointer = self.currentPointer.parent
            self.float_node(node=node)
        else:
            node.children.append(self.currentPointer.children.pop())
            self.currentPointer.children.append(node)
            self.currentPointer = node

    def reset(self):
        self.root = None
        self.currentPointer = None

    def update_values(self, node: Node):
        for c in node.children:
            self.update_values(node=c)
        node.value = node()

    def update_dims(self, node: Node):
        if len(node.children) > 0:
            for c in node.children:
                self.update_dims(c)
            node.width = sum(map(lambda n: n.width, node.children)
                             ) + (len(node.children) - 1) * self.padding
            node.height = max(map(lambda n: n.height, node.children)) + 1

    def generate_tmp_nodes(self, node: Node, depth: int = 1):
        if len(node.children) > 0:
            for c in node.children:
                self.generate_tmp_nodes(node=c, depth=depth + 1)
        elif depth < cast(Node, self.root).height:
            self.attach_tmp_node(node=node, depth=depth)

    def attach_tmp_node(self, node: Node, depth: int):
        total_height = cast(Node, self.root).height
        for _ in range(total_height - depth):
            node = Temp_Node(parent=node)

    def prune_tmp_nodes(self, node: Node):
        if len(node.children) > 0 and isinstance(node.children[0], Temp_Node):
            node.children.pop()
        for c in node.children:
            self.prune_tmp_nodes(node=c)

    def update(self, which: Literal['all', 'dimensions', 'values'] = 'all'):
        if self.root is not None:
            if which != 'dimensions':
                self.update_values(node=self.root)
            if which != 'values':
                self.update_dims(node=self.root)
            if which not in ['all', 'dimensions', 'values']:
                raise UpdateTreeError(
                    f'Unexpected value \'{which}\' for \'which\' parameter encountered')

    def __enter__(self):
        if self.root is None:
            raise UpdateTreeError('Root is None')
        self.generate_tmp_nodes(node=self.root)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.root is None:
            raise UpdateTreeError('Root is None')
        self.prune_tmp_nodes(node=self.root)

    def __str__(self):
        self.update(which='dimensions')
        if self.root is not None:
            current_children: List[List[Node]] = [[self.root]]
            next_children: List[List[Node]] = []
            result = ''
            with self:
                while len(current_children[0]) > 0:
                    for n_ls in current_children:
                        for n in n_ls:
                            result += str(n) + ' ' * self.padding
                            next_children.append(n.children)
                    result += '\n'
                    current_children = next_children
                    next_children = []
                    for n_ls in current_children:
                        no_of_children = len(n_ls)
                        if no_of_children == 1:
                            n = n_ls[0]
                            if isinstance(n, Temp_Node):
                                result += str(n) + ' '
                            else:
                                result += f'{self.middle_branch:^{n.width}} '
                        elif no_of_children > 1:
                            result += f'{self.left_branch:^{n_ls[0].width}} '
                            for n in n_ls[1:-1]:
                                result += f'{self.middle_branch:^{n.width}} '
                            result += f'{self.right_branch:^{n_ls[-1].width}} '
                    result += '\n'
            # Remove 2 redundant newline characters at end of string
            return result[:-2]
        raise TreeReprError('Empty Tree Encountered')

    def __call__(self):
        pass
