class Rectangle:
   
    def __init__(self, x, y, width, height):
        # x and y represent the center of the rectangle
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point):
        """Check if a point (x, y) is inside this boundary."""
        return (self.x - self.width <= point[0] < self.x + self.width and
                self.y - self.height <= point[1] < self.y + self.height)

    def intersects(self, range_rect):
        """Check if a given viewing range intersects this boundary."""
        return not (range_rect.x - range_rect.width > self.x + self.width or
                    range_rect.x + range_rect.width < self.x - self.width or
                    range_rect.y - range_rect.height > self.y + self.height or
                    range_rect.y + range_rect.height < self.y - self.height)

class QuadTree:
    """The QuadTree acceleration structure for LOD and Culling."""
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = [] # In your case, these would be terrain chunks or vertices
        self.divided = False

    def subdivide(self):
        """Split the current node into four quadrants."""
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width / 2
        h = self.boundary.height / 2

        ne = Rectangle(x + w, y - h, w, h)
        nw = Rectangle(x - w, y - h, w, h)
        se = Rectangle(x + w, y + h, w, h)
        sw = Rectangle(x - w, y + h, w, h)

        self.northeast = QuadTree(ne, self.capacity)
        self.northwest = QuadTree(nw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        
        self.divided = True

    def insert(self, point):
        """Insert a terrain chunk or vertex into the QuadTree."""
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northeast.insert(point): return True
            if self.northwest.insert(point): return True
            if self.southeast.insert(point): return True
            if self.southwest.insert(point): return True

    def query(self, range_rect, found_points=None):
        """Return only the points/chunks that fall within a specific viewing range (Camera View)."""
        if found_points is None:
            found_points = []

        if not self.boundary.intersects(range_rect):
            return found_points

        for p in self.points:
            if range_rect.contains(p):
                found_points.append(p)

        if self.divided:
            self.northeast.query(range_rect, found_points)
            self.northwest.query(range_rect, found_points)
            self.southeast.query(range_rect, found_points)
            self.southwest.query(range_rect, found_points)

        return found_points
