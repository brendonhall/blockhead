import numpy as np
import unittest

from blockhead.interval_tree import IntervalNode


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
        self.root.add_child(IntervalNode(44, 0, 512, self.contour_1))

        self.contour_2 = {
            'max_scale': 40,
            'location1': 600,
            'location2': 700,
            'id': 2,
            'data': [4, 5, 6]
        }
        self.root.add_child(IntervalNode(40, 512, 1024, self.contour_2))

    def test_get_interval(self):
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
        np.testing.assert_array_equal(contour['data'], self.contour_2['data'])

    def test_contains(self):
        self.assertTrue(self.root.contains(self.contour_1))
        self.assertTrue(self.root.contains(self.contour_2))

        children = self.root.get_children()
        self.assertTrue(children[0].contains(self.contour_1))
        self.assertFalse(children[0].contains(self.contour_2))
        self.assertFalse(children[1].contains(self.contour_1))
        self.assertTrue(children[1].contains(self.contour_2))
