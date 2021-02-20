from math import sin, cos


class PositionTransform:
    # Matrix will be 3x3 Matrix [row][column]
    matrix = None

    def __init__(self):
        self.identity()

    def identity(self):
        self.matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def copy(self, t):
        self.matrix = [
            [t.matrix[0][0], t.matrix[0][1], t.matrix[0][2]],
            [t.matrix[1][0], t.matrix[1][1], t.matrix[1][2]],
            [t.matrix[2][0], t.matrix[2][1], t.matrix[2][2]]]

    def print(self):
        print(self.matrix)

    def transform(self, coord):
        transformed = (
            # X' = M[0][0]X + M[1][0]Y + m[2][0]
            coord[0] * self.matrix[0][0] + coord[1] * self.matrix[1][0] + self.matrix[2][0],
            # Y' = M[0][1]X + M[1][1]Y + m[2][1]
            coord[0] * self.matrix[0][1] + coord[1] * self.matrix[1][1] + self.matrix[2][1])
        return transformed

    def combine(self, transform):
        result = PositionTransform()

        # Matrix Multiply
        result.matrix[0][0] = self.matrix[0][0] * transform.matrix[0][0] + \
                              self.matrix[0][1] * transform.matrix[1][0] + \
                              self.matrix[0][2] * transform.matrix[2][0]
        result.matrix[0][1] = self.matrix[0][0] * transform.matrix[0][1] + \
                              self.matrix[0][1] * transform.matrix[1][1] + \
                              self.matrix[0][2] * transform.matrix[2][1]
        result.matrix[0][2] = self.matrix[0][0] * transform.matrix[0][2] + \
                              self.matrix[0][1] * transform.matrix[1][2] + \
                              self.matrix[0][2] * transform.matrix[2][2]
        result.matrix[1][0] = self.matrix[1][0] * transform.matrix[0][0] + \
                              self.matrix[1][1] * transform.matrix[1][0] + \
                              self.matrix[1][2] * transform.matrix[2][0]
        result.matrix[1][1] = self.matrix[1][0] * transform.matrix[0][1] + \
                              self.matrix[1][1] * transform.matrix[1][1] + \
                              self.matrix[1][2] * transform.matrix[2][1]
        result.matrix[1][2] = self.matrix[1][0] * transform.matrix[0][2] + \
                              self.matrix[1][1] * transform.matrix[1][2] + \
                              self.matrix[1][2] * transform.matrix[2][2]
        result.matrix[2][0] = self.matrix[2][0] * transform.matrix[0][0] + \
                              self.matrix[2][1] * transform.matrix[1][0] + \
                              self.matrix[2][2] * transform.matrix[2][0]
        result.matrix[2][1] = self.matrix[2][0] * transform.matrix[0][1] + \
                              self.matrix[2][1] * transform.matrix[1][1] + \
                              self.matrix[2][2] * transform.matrix[2][1]
        result.matrix[2][2] = self.matrix[2][0] * transform.matrix[0][2] + \
                              self.matrix[2][1] * transform.matrix[1][2] + \
                              self.matrix[2][2] * transform.matrix[2][2]
        return result

    def inverse(self):
        res = PositionTransform()
        det = self._get_determinant()
        if det != 0:
            inv_det = 1 / det
            res.matrix[0][0] = (self.matrix[1][1] * self.matrix[2][2] - self.matrix[2][1] * self.matrix[1][2]) * inv_det
            res.matrix[0][1] = (self.matrix[0][2] * self.matrix[2][1] - self.matrix[0][1] * self.matrix[2][2]) * inv_det
            res.matrix[0][2] = (self.matrix[0][1] * self.matrix[1][2] - self.matrix[0][2] * self.matrix[1][1]) * inv_det
            res.matrix[1][0] = (self.matrix[1][2] * self.matrix[2][0] - self.matrix[1][0] * self.matrix[2][2]) * inv_det
            res.matrix[1][1] = (self.matrix[0][0] * self.matrix[2][2] - self.matrix[0][2] * self.matrix[2][0]) * inv_det
            res.matrix[1][2] = (self.matrix[1][0] * self.matrix[0][2] - self.matrix[0][0] * self.matrix[1][2]) * inv_det
            res.matrix[2][0] = (self.matrix[1][0] * self.matrix[2][1] - self.matrix[2][0] * self.matrix[1][1]) * inv_det
            res.matrix[2][1] = (self.matrix[2][0] * self.matrix[0][1] - self.matrix[0][0] * self.matrix[2][1]) * inv_det
            res.matrix[2][2] = (self.matrix[0][0] * self.matrix[1][1] - self.matrix[1][0] * self.matrix[0][1]) * inv_det
        return res

    def _get_determinant(self):
        det = \
            self.matrix[0][0] * (self.matrix[1][1] * self.matrix[2][2] - self.matrix[2][1] * self.matrix[1][2]) - \
            self.matrix[0][1] * (self.matrix[1][0] * self.matrix[2][2] - self.matrix[1][2] * self.matrix[2][0]) + \
            self.matrix[0][2] * (self.matrix[1][0] * self.matrix[2][1] - self.matrix[1][1] * self.matrix[2][0])
        return det


class Shift(PositionTransform):
    def __init__(self, x_offset, y_offset):
        PositionTransform.__init__(self)
        self.matrix[2][0] = x_offset
        self.matrix[2][1] = y_offset


class Scale(PositionTransform):
    def __init__(self, scale):
        PositionTransform.__init__(self)
        self.matrix[0][0] = scale
        self.matrix[1][1] = scale


class Rotation(PositionTransform):
    def __init__(self, angle):
        PositionTransform.__init__(self)
        self.matrix[0][0] = cos(angle)
        self.matrix[1][0] = -sin(angle)
        self.matrix[0][1] = sin(angle)
        self.matrix[1][1] = cos(angle)


class HorizontalFlip(PositionTransform):
    def __init__(self):
        PositionTransform.__init__(self)
        self.matrix[1][1] = -1


class SamplePointTransform(PositionTransform):
    """ From Sample Points p1->pa, p2->pb, p3->pc """
    def __init__(self, p1, p2, p3, pa, pb, pc):
        PositionTransform.__init__(self)
        start = PositionTransform()
        start.matrix = [
            [p1[0], p1[1], 1],
            [p2[0], p2[1], 1],
            [p3[0], p3[1], 1]]
        end = PositionTransform()
        end.matrix = [
            [pa[0], pa[1], 1],
            [pb[0], pb[1], 1],
            [pc[0], pc[1], 1]]
        start_inv = start.inverse()
        res = start_inv.combine(end)
        self.copy(res)
