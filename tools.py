# not using KDTree for this project but might be useful.
class KDTree:
    def __init__(self, point=None):
        self.point = point
        self.left = None
        self.right = None

    def build_tree(self, points):
        if not points:
            print("need points to build")
            return

        while points:
            point = points.pop()
            self.add_point(point)

    def add_point(self, point):
        xdir = True

        if self.point is None:
            self.point = point
        else:
            tmp = self
            while tmp.point is not None:

                if xdir:
                    xdir = False
                    ix = 0
                else:
                    xdir = True
                    ix = 1
                # The if else above is so we switch between looking at x and y direction.
                if point[ix] < tmp.point[ix]:
                    if tmp.left is None:
                        tmp.left = KDTree(point)
                        break
                    else:
                        tmp = tmp.left
                else:
                    if tmp.right is None:
                        tmp.right = KDTree(point)
                        break
                    else:
                        tmp = tmp.right


