import numpy as np
import unittest

from blockhead.interval_tree import (IntervalNode,
                                     preOrderTraversal,
                                     get_parent_interval)


class IntervalNodeTestCase(unittest.TestCase):
    def setUp(self):
        self.empty_tree = IntervalNode(50, 0, 1024, None)

        self.root = IntervalNode(50, 0, 1024, None)
        self.contour_1 = {
            'max_scale': 35,
            'location1': 10,
            'location2': 256,
            'id': 1,
            'data': [1, 2, 3]
        }
        node = IntervalNode(44, 0, 512, self.contour_1)

        self.contour_2 = {
            'max_scale': 35,
            'location1': 110,
            'location2': 200,
            'id': 2,
            'data': [3, 4, 5]
        }
        node.add_child(IntervalNode(30, 100, 200, self.contour_2))
        self.root.add_child(node)

        self.contour_3 = {
            'max_scale': 40,
            'location1': 600,
            'location2': 700,
            'id': 2,
            'data': [4, 5, 6]
        }
        node = IntervalNode(40, 512, 1024, self.contour_3)

        self.contour_4 = {
            'max_scale': 30,
            'location1': 650,
            'location2': 660,
            'id': 3,
            'data': [4, 5, 6]
        }
        node.add_child(IntervalNode(30, 600, 700, self.contour_4))
        self.root.add_child(node)

    def test_get_children(self):
        children = self.empty_tree.get_children()
        self.assertEqual(len(children), 0)

        children = self.root.get_children()
        self.assertEqual(len(children), 2)

        self.assertEqual(children[0].scale, 44)
        self.assertEqual(children[0].top_edge, 0)
        self.assertEqual(children[0].bottom_edge, 512)
        contour = children[0].contour
        np.testing.assert_array_equal(contour['data'], self.contour_1['data'])

        self.assertEqual(children[1].scale, 40)
        self.assertEqual(children[1].top_edge, 512)
        self.assertEqual(children[1].bottom_edge, 1024)
        contour = children[1].contour
        np.testing.assert_array_equal(contour['data'], self.contour_3['data'])

    def test_contains(self):
        self.assertTrue(self.root.contains(self.contour_1))
        self.assertTrue(self.root.contains(self.contour_3))

        children = self.root.get_children()
        self.assertTrue(children[0].contains(self.contour_1))
        self.assertFalse(children[0].contains(self.contour_3))
        self.assertFalse(children[1].contains(self.contour_1))
        self.assertTrue(children[1].contains(self.contour_3))

    def test_get_interval(self):
        children = self.root.get_children()
        interval = children[0].get_interval()
        top_edge, bottom_edge = interval
        self.assertEqual(top_edge, 0)

        interval = children[1].get_interval()
        top_edge, bottom_edge = interval
        self.assertEqual(bottom_edge, 1024)

    def test_has_children(self):
        self.assertTrue(self.root.has_children())
        self.assertFalse(self.empty_tree.has_children())

    def test_get_data(self):
        data = self.root.get_data()
        self.assertEqual(data['scale'], 50)
        self.assertEqual(data['top'], 0)
        self.assertEqual(data['bottom'], 1024)

    def test_preOrderTraversal(self):
        result = preOrderTraversal(self.root)

        np.testing.assert_equal(
            [i['scale'] for i in result], [50, 44, 30, 40, 30]
        )
        np.testing.assert_equal(
            [i['top'] for i in result], [0, 0, 100, 512, 600]
        )
        np.testing.assert_equal(
            [i['bottom'] for i in result], [1024, 512, 200, 1024, 700]
        )

    def test_parent_interval(self):
        contour_5 = {
            'max_scale': 25,
            'location1': 125,
            'location2': 135,
            'id': 101,
            'data': [100, 200, 300]
        }
        result = get_parent_interval(self.root, contour_5)
        # The parent of a node that contains this interval
        self.assertEqual(result.scale, 30)
        self.assertEqual(result.top_edge, 100)
        self.assertEqual(result.bottom_edge, 200)
