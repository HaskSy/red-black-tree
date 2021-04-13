from __future__ import annotations
from enum import Enum
from typing import Callable


def _default_cmp(a, b):
    return (a > b) - (a < b)


class Color(Enum):
    BLACK = False
    RED = True


class RBTreeNode:

    def __init__(self,
                 value=None,
                 color: Color = Color.BLACK,
                 left: RBTreeNode = None,
                 right: RBTreeNode = None,
                 parent: RBTreeNode = None,
                 ) -> None:
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.color = color

    def __bool__(self):
        return self is not None and self.value is not None


class RBTree:

    def __init__(self, comparator: Callable = _default_cmp):
        self.root = None
        self.size = 0
        self.cmp = comparator

    def __iter__(self):
        yield from RBTIterator(self).nodes

    def insert(self, value) -> None:
        if value is None:
            raise Exception("Input value cannot be None")

        if not self.root:
            self.root = RBTreeNode(value, left=None, right=None)
            # Where None - leaf (Black)
            self.size += 1
            return

        node = RBTreeNode(value, color=Color.RED, left=None, right=None, parent=None)

        pointer = self.root
        parent = None

        # finding a parent node
        while pointer:
            parent = pointer
            if self.cmp(node.value, parent.value) == 0:
                return  # value already contains in the tree

            elif self.cmp(pointer.value, node.value) < 0:
                pointer = pointer.right

            else:
                pointer = pointer.left

        node.parent = parent

        if self.cmp(parent.value, node.value) < 0:
            parent.right = node
        else:
            parent.left = node

        self.__fix_coloring(node)
        self.size += 1

    def find(self, value) -> RBTreeNode:
        root = self.root
        while True:
            if root is None:  # this value not in the tree
                return
            if self.cmp(value, root.value) > 0:
                root = root.right
            elif self.cmp(value, root.value) < 0:
                root = root.left
            else:
                break
        return root

    def black_height(self, value) -> int:
        """
        height counts black nodes starting with Node(value) and doesn't count last NIL node
        """
        root = self.find(value)
        height = 0

        if root is None:  # this value not in the tree
            return

        while True:
            if root.color is Color.BLACK:
                height += 1

            if root.left:
                root = root.left
            elif root.right:
                root = root.right
            else:
                return height

    def contains(self, value) -> bool:
        return bool(self.find(value))

    def vertices_count(self) -> int:
        return self.size

    def __fix_coloring(self, node: RBTreeNode) -> None:

        """
        if node.parent is root or node color is black or parent color is black,
        then there is no need to fix anything
        """
        if node.parent.parent is None \
                or node.color is Color.BLACK \
                or node.parent.color is Color.BLACK:
            return

        while node.parent and node.parent.color is Color.RED:  # is red

            # parent = node.parent, grandparent = parent.parent

            if node.parent == node.parent.parent.left:

                uncle = node.parent.parent.right

                if uncle and uncle.color is Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent

                else:  # uncle doesn't exist or black
                    if node == node.parent.right:
                        node = node.parent
                        self.__left_rotate(node)

                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self.__right_rotate(node.parent.parent)

            else:  # parent == grandparent.right

                uncle = node.parent.parent.left
                if uncle and uncle.color is Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent

                else:  # uncle doesn't exist or black
                    if node == node.parent.left:
                        node = node.parent
                        self.__right_rotate(node)

                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self.__left_rotate(node.parent.parent)

        self.root.color = Color.BLACK

    def __left_rotate(self, node: RBTreeNode) -> None:

        tmp = node.right

        node.right = tmp.left
        if tmp.left:
            tmp.left.parent = node

        if tmp:
            tmp.parent = node.parent

        if node.parent:
            if node == node.parent.left:
                node.parent.left = tmp
            else:
                node.parent.right = tmp
        else:
            self.root = tmp

        tmp.left = node
        if node:
            node.parent = tmp

    def __right_rotate(self, node: RBTreeNode) -> None:

        tmp = node.left

        node.left = tmp.right
        if tmp.right:
            tmp.right.parent = node

        if tmp:
            tmp.parent = node.parent

        if node.parent:
            if node == node.parent.right:
                node.parent.right = tmp
            else:
                node.parent.left = tmp
        else:
            self.root = tmp

        tmp.right = node
        if node:
            node.parent = tmp


class RBTIterator(RBTree):
    def __init__(self, tree: RBTree):
        super().__init__()
        self.root = tree.root
        self.nodes = []
        self.index = -1
        self.traverse(self.root)

    def traverse(self, root) -> None:
        if not root:
            return
        self.traverse(root.left)
        self.nodes.append(root)
        self.traverse(root.right)

    def next(self) -> RBTreeNode:
        self.index += 1
        return self.nodes[self.index]

    def has_next(self) -> bool:
        return self.index < len(self.nodes) - 1
