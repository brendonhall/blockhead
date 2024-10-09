class IntervalNode(object):
    def __init__(self, scale, top_edge, bottom_edge, contour):
        self.scale = scale
        self.top_edge = top_edge
        self.bottom_edge = bottom_edge
        self.contour = contour
        self.children = []

    def __str__(self):
        string = \
            f"Interval scale: {self.scale:.1f} top: {self.top_edge:.1f},bottom: {self.bottom_edge:.1f}, children: {self.children}"  # noqa
        return string

    def __repr__(self):
        return f"Scale: {self.scale:.1f}[{self.top_edge:.1f},{self.bottom_edge:.1f}]"  # noqa

    def add_child(self, obj):
        self.children.append(obj)

    def has_children(self):
        return len(self.children) > 0

    def get_children(self):
        return self.children

    def get_interval(self):
        return (self.top_edge, self.bottom_edge)

    def get_data(self):
        data = {'scale': self.scale, 'top': self.top_edge, 'bottom': self.bottom_edge}  # noqa
        return data

    def contains(self, contour):
        is_in = False
        if((contour['location1'] > self.top_edge) &
           (contour['location1'] < self.bottom_edge)):
            if contour['location2']:
                if((contour['location2'] > self.top_edge) &
                   (contour['location2'] < self.bottom_edge)):
                    is_in = True
            else:
                is_in = True
        return is_in


def preOrderTraversal(node):
    res = []
    if node:
        res.append(node.get_data())
        for child in node.get_children():
            res = res + preOrderTraversal(child)
    return res


def get_parent_interval(node, contour):
    """algo to traverse the tree, and find the parent interval (node)
        for each contour to be added. if current node contains the contour,
        and has no children, then return current node.

        Parameters
        ----------

        node: IntervalNode
            A node in the interval tree containing a contour.

        contour: dict, with fields
            'max_scale': the max scale that the contour is visible at.
            'location1': the top location.
            'location2': the bottom location.
            'id': an auto incrementing counter.
            'data': the path of the contour in the scale space.

        Returns
        -------
        parent_int: IntervalNode or None
            If the node has a parent, return the parent, else
            return None.
    """
    if node.contains(contour) & ~node.has_children():
        return node
    # if current node contains the contour, but has children,
    # then find the parent interaval among the children
    elif node.contains(contour) & node.has_children():
        for child in node.get_children():
            parent_int = get_parent_interval(child, contour)
            if parent_int:
                return parent_int
    else:
        return None
