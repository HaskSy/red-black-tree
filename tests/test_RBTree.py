import unittest

from src.RBTree import *
from src.RBTree import _default_cmp


class TestRBTree(unittest.TestCase):

    def test_default_cmp(self):
        self.assertEqual(_default_cmp(3, 5), -1)
        self.assertEqual(_default_cmp(10, 3), 1)
        self.assertEqual(_default_cmp(5, 5), 0)

    def test_search(self):
        rb_tree = RBTree()
        rb_tree.insert(-5)
        node_n5 = rb_tree.root
        rb_tree.insert(-13)
        node_n13 = rb_tree.root.left
        rb_tree.insert(4)
        node_4 = rb_tree.root.right
        rb_tree.insert(5)
        node_5 = node_4.right
        rb_tree.insert(13)
        node_13 = node_5.right
        rb_tree.insert(3)
        node_3 = node_4.left
        rb_tree.insert(6)
        node_6 = node_13.left
        rb_tree.insert(7)
        node_7 = node_5.right
        rb_tree.insert(23)
        node_23 = node_13.right

        self.assertEqual(rb_tree.find(5), node_5)
        self.assertEqual(rb_tree.find(-13), node_n13)
        self.assertEqual(rb_tree.find(3), node_3)
        self.assertEqual(rb_tree.find(7), node_7)
        self.assertEqual(rb_tree.find(6), node_6)
        self.assertEqual(rb_tree.find(-5), node_n5)
        self.assertEqual(rb_tree.find(13), node_13)
        self.assertEqual(rb_tree.find(23), node_23)
        self.assertEqual(rb_tree.find(4), node_4)

        self.assertIsNone(rb_tree.find(-143))
        self.assertIsNone(rb_tree.find(52454225))
        self.assertIsNone(rb_tree.find(70))
        self.assertIsNone(rb_tree.find(4101))
        self.assertIsNone(rb_tree.find(600001))

    def test_contains(self):
        rb_tree = RBTree()

        array = [-82, 29, 20, 21, -23, 52, 60, 70, 31, 49, -51, -43, -42, -40, 6, 12, 19, 91, 93, -61, -60, -52, -2, 2]

        for elem in array:
            rb_tree.insert(elem)

        for elem in array:
            self.assertTrue(rb_tree.contains(elem))

        self.assertFalse(rb_tree.contains(0))
        self.assertFalse(rb_tree.contains(-55))
        self.assertFalse(rb_tree.contains(100))
        self.assertFalse(rb_tree.contains(99))
        self.assertFalse(rb_tree.contains(422))

    def test_right_rotation(self):
        rb_tree = RBTree()
        root = RBTreeNode(value=10, color=Color.BLACK, parent=None)

        # LEFT SUBTREE
        node_n10 = RBTreeNode(value=-10, color=Color.BLACK, parent=root, left=None, right=None)
        node_7 = RBTreeNode(value=7, color=Color.RED, parent=node_n10, left=None, right=None)
        node_n10.right = node_7

        # RIGHT SUBTREE
        node_20 = RBTreeNode(value=20, color=Color.BLACK, parent=root, left=None, right=None)
        node_15 = RBTreeNode(value=15, color=Color.RED, parent=node_20, left=None, right=None)
        node_20.left = node_15

        root.left = node_n10
        root.right = node_20

        rb_tree.root = root
        rb_tree.insert(13)

        expected_values = [-10, 7, 10, 13, 15, 20]
        values = list(map(lambda x: x.value, rb_tree))
        self.assertEqual(expected_values, values)

        node_20 = node_15.right
        node_13 = node_15.left

        self.assertEqual(node_15.color, Color.BLACK)
        self.assertEqual(node_15.parent.value, 10)

        self.assertEqual(node_20.value, 20)
        self.assertEqual(node_20.color, Color.RED)
        self.assertEqual(node_20.parent.value, 15)
        self.assertEqual(node_20.left, None)
        self.assertEqual(node_20.right, None)

        self.assertEqual(node_13.value, 13)
        self.assertEqual(node_13.color, Color.RED)
        self.assertEqual(node_13.parent.value, 15)
        self.assertEqual(node_13.left, None)
        self.assertEqual(node_13.right, None)

    def test_left_rotation(self):
        rb_tree = RBTree()
        root = RBTreeNode(value=10, color=Color.BLACK, parent=None, left=None, right=None)
        # LEFT SUBTREE
        node_7 = RBTreeNode(value=7, color=Color.BLACK, parent=root, left=None, right=None)
        node_8 = RBTreeNode(value=8, color=Color.RED, parent=node_7, left=None, right=None)
        node_7.right = node_8

        # RIGHT SUBTREE
        rightest = RBTreeNode(value=20, color=Color.BLACK, parent=root, left=None, right=None)
        root.left = node_7
        root.right = rightest

        rb_tree.root = root
        rb_tree.insert(9)

        expected_values = [7, 8, 9, 10, 20]
        values = list(map(lambda x: x.value, rb_tree))
        self.assertEqual(expected_values, values)

        node_9 = node_8.right

        self.assertEqual(node_9.value, 9)
        self.assertEqual(node_9.color, Color.RED)
        self.assertEqual(node_9.parent.value, 8)
        self.assertEqual(node_9.left, None)
        self.assertEqual(node_9.right, None)

        self.assertEqual(node_8.parent.value, 10)
        self.assertEqual(node_8.color, Color.BLACK)
        self.assertEqual(node_8.left.value, 7)
        self.assertEqual(node_8.right.value, 9)

        self.assertEqual(node_7.color, Color.RED)
        self.assertEqual(node_7.parent.value, 8)
        self.assertEqual(node_7.left, None)
        self.assertEqual(node_7.right, None)


if __name__ == '__main__':
    unittest.main()
