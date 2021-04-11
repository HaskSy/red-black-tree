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
        return self.value is not None


class RBTree:

    def __init__(self, comparator=_default_cmp):
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

    def find(self, value):
        root = self.root
        while root is not None:
            if self.cmp(value, root.value) > 0:
                root = root.right
            elif self.cmp(value, root.value) < 0:
                root = root.left
            else:
                break
        return root

    def contains(self, value) -> bool:
        return bool(self.find(value))

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

            # made just for a bit more comfortable code reading
            parent = node.parent
            grandparent = parent.parent

            if parent == grandparent.left:

                uncle = grandparent.right

                if uncle and uncle.color is Color.RED:
                    parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    grandparent.color = Color.RED
                    node = grandparent

                else:  # uncle doesn't exist or black
                    if node == parent.right:
                        node = parent
                        self.__left_rotate(node)

                    parent.color = Color.BLACK
                    grandparent.color = Color.RED
                    self.__right_rotate(grandparent)

            else:  # parent == grandparent.right

                uncle = grandparent.left
                if uncle and uncle.color is Color.RED:
                    parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    grandparent.color = Color.RED
                    node = grandparent

                else:  # uncle doesn't exist or black
                    if node == parent.left:
                        node = parent
                        self.__right_rotate(node)

                    parent.color = Color.BLACK
                    grandparent.color = Color.RED
                    self.__left_rotate(grandparent)

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

    def traverse(self, root):
        if not root:
            return
        self.traverse(root.left)
        self.nodes.append(root)
        self.traverse(root.right)

    def next(self) -> int:
        self.index += 1
        return self.nodes[self.index]

    def has_next(self) -> bool:
        return self.index < len(self.nodes) - 1
