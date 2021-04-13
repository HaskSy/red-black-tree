import unittest
import random

from src.RBTree import *


class TestRandomInputs(unittest.TestCase):

    def test_NoneType_issues(self, n=20):
        """
        testing insertion on 20 different 25 or less length random arrays of data

        Check on taking attributes from NoneType
        """
        for _ in range(n):
            array = list(set(random.randint(-100, 100) for _ in range(25)))  # non-duplicative values (25 or less)
            rb_tree = RBTree()
            for elem in array:
                rb_tree.insert(elem)

            array.sort()
            print(array)
            values = list(map(lambda x: x.value, rb_tree))
            self.assertEqual(array, values)

    def test_coloring(self, n=20):
        """
        Testing all Red-black binary tree properties
        """

        def height_helper(tree_node: RBTreeNode):
            """
            A recursive function which count black_height for each path to leaf from selected node
            """

            if not tree_node:
                return 0

            left = height_helper(tree_node.left)

            right = height_helper(tree_node.right)

            height = 1 if tree_node.color is Color.BLACK else 0

            if left == -1 or right == -1 or left != right:
                return -1
            else:
                return left + height

        for _ in range(n):
            array = list(set(random.randint(-100, 100) for _ in range(25)))  # non-duplicative values (25 or less)
            rb_tree = RBTree()
            for elem in array:
                rb_tree.insert(elem)

            self.assertEqual(rb_tree.root.color, Color.BLACK)  # root is black

            # There is no need to check if every leaf is black,
            # because every leaf is None and behaves like black-colored node in this implementation

            tree_iterator = RBTIterator(rb_tree)
            while tree_iterator.has_next():
                node = tree_iterator.next()

                if node.color is Color.RED:  # If a node is red, then both its children are black.
                    if node.left:
                        self.assertEqual(node.left.color, Color.BLACK)
                    if node.right:
                        self.assertEqual(node.right.color, Color.BLACK)

                # Black height equality
                self.assertTrue(height_helper(node) != -1)


if __name__ == '__main__':
    unittest.main()
