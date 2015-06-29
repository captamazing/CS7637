class Object:

    def __init__(self, xy, l_val):
        self.l_val = l_val
        self.area = [xy]
        self.centroid = (0, 0)
        self.max_x = 0
        self.min_x = 9999
        self.max_y = 0
        self.min_y = 9999

    def add_pixel(self, xy):
        self.area.append(xy)
        if xy[0] > self.max_x:
            self.max_x = xy[0]
        if xy[0] < self.min_x:
            self.min_x = xy[0]
        if xy[1] > self.max_y:
            self.max_y = xy[1]
        if xy[1] < self.min_y:
            self.min_y = xy[1]

    def remove_pixel(self, xy):
        self.area.remove(xy)

    def find_centroid(self):
        x_total = 0
        y_total = 0

        for pixel in self.area:
            x_total += pixel[0]
            y_total += pixel[1]

        x_cen = round(x_total / len(self.area), 0)
        y_cen = round(y_total / len(self.area), 0)

        self.centroid = (x_cen, y_cen)
        return self.centroid

    def size(self):
        width = self.max_x - self.min_x + 1
        height = self.max_y - self.min_y + 1
        return (width, height)