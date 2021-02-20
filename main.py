from transform import PositionTransform, SamplePointTransform, Scale, HorizontalFlip, Shift, Rotation
import math


def main():
    scale = Scale(2)
    shift = Shift(10, 20)
    rotate = Rotation(math.pi/2)
    combined = PositionTransform()
    combined = combined.combine(scale)
    combined = combined.combine(shift)
    combined = combined.combine(rotate)
    combined.print()

    p1 = (1, 1)
    p2 = (1, 2)
    p3 = (2, 5)
    pa = combined.transform(p1)
    pb = combined.transform(p2)
    pc = combined.transform(p3)

    print(p1)
    print(p2)
    print(p3)

    print(pa)
    print(pb)
    print(pc)

    test_inverse = combined.inverse()
    test_inverse.print()

    p4 = test_inverse.transform(pa)
    p5 = test_inverse.transform(pb)
    p6 = test_inverse.transform(pc)

    print(p4)
    print(p5)
    print(p6)

    test = SamplePointTransform(p1, p2, p3, pa, pb, pc)
    test.print()

    coord = (1, 1)
    coord2 = test.transform(coord)
    print(coord)
    print(coord2)


if __name__ == "__main__":
    main()
