from __future__ import annotations


class RBTreeNode:

    def __init__(self,
                 value=None,
                 color: bool = False,
                 left: RBTreeNode = None,
                 right: RBTreeNode = None,
                 parent: RBTreeNode = None,
                 ) -> None:
        """ False - black node, True - red node"""
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.color = color


class RBTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, value) -> None:
        if self.root is None:
            self.root = RBTreeNode(value, left=RBTreeNode(), right=RBTreeNode())
            # Where RBTreeNode() - NIL leaf (Black)
            self.size += 1
            return

        node = RBTreeNode(value, color=True, left=RBTreeNode(), right=RBTreeNode())

        pointer = self.root
        parent = None

        # finding a parent node
        while pointer.value is not None:
            parent = pointer
            if node.value == parent.value:
                return  # value already contains in the tree

            elif pointer.value < node.value:
                pointer = pointer.right

            else:
                pointer = pointer.left

        node.parent = parent

        if parent.value < node.value:
            parent.right = node
        else:
            parent.left = node

        self.__fix_coloring(node)
        self.size += 1

    def __fix_coloring(self, node: RBTreeNode) -> None:

        """
        if node.parent is root or node color is black or parent color is black,
        then there is no need to fix anything
        """
        if node.parent.parent is None \
                or node.color is False \
                or node.parent.color is False:
            return

        while node.parent.color is True:  # is red

            # made just for a bit more comfortable code reading
            parent = node.parent
            grandparent = parent.parent

            if parent == grandparent.left:
                uncle = grandparent.right

                if uncle.value is not None:
                    if uncle.color is True:
                        parent.color = False
                        uncle.color = False
                        grandparent.color = True
                        node = grandparent

                else:  # uncle.value is None
                    if node == parent.right:
                        node = parent
                        self.__left_rotate(node)
                    parent.color = False
                    grandparent.color = True
                    self.__right_rotate(grandparent)

            else:  # parent == grandparent.right
                uncle = grandparent.left

                if uncle.value is not None:
                    if uncle.color is True:
                        parent.color = False
                        uncle.color = False
                        grandparent.color = True
                        node = grandparent

                else:  # uncle.value is None
                    if node == parent.right:
                        node = parent
                        self.__right_rotate(node)
                    parent.color = False
                    grandparent.color = True
                    self.__left_rotate(grandparent)

        self.root.color = False

    def __left_rotate(self, node: RBTreeNode) -> None:

        right_child = node.right
        node.right = right_child.left
        if right_child.left != RBTreeNode():
            right_child.left.parent = node
        right_child.parent = node.parent

        if node.parent != RBTreeNode():
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def __right_rotate(self, node: RBTreeNode) -> None:

        left_child = node.left
        node.left = left_child.right
        if left_child.right != RBTreeNode():
            left_child.right.parent = node
        left_child.parent = node.parent

        if node.parent != RBTreeNode():
            self.root = left_child
        elif node == node.parent.left:
            node.parent.left = left_child
        else:
            node.parent.right = left_child

        left_child.right = node
        node.parent = left_child
