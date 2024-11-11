import dataclasses

import math

type Point = Anchor | Intersect
type Distance = float


def sqrt(x):
    return math.sqrt(x)


"""
An anchor is a special type of Location,
given by a concrete location, specifically,
the edges of our canvas."""


@dataclasses.dataclass
class Anchor:
    x: int
    y: int


"""
where TWO lines meet.
"""


@dataclasses.dataclass
class Intersect:
    l1: "Line|Circle"
    l2: "Line|Circle"


# a line is given by two points.
@dataclasses.dataclass
class Line:
    p1: Point
    p2: Point

    def get_mxb(self) -> tuple[float, float]:
        p1_a = get_location(self.p1)
        p2_a = get_location(self.p2)
        m = (p2_a.y - p1_a.y) / (p2_a.x - p1_a.x)
        b = p1_a.y - m * p1_a.x
        return m, b


@dataclasses.dataclass
class Circle:
    center: Point
    radius: Distance


import chaos_math


def get_location(obj: Point | Line | Circle) -> Anchor:
    match obj:
        case Anchor():
            return obj
        case Intersect():
            match obj.l1, obj.l2:
                case Line(), Line():
                    l1 = obj.l1
                    l2 = obj.l2
                    a, b = l1.get_mxb()
                    c, d = l2.get_mxb()
                    if a == c and d == b:
                        return True
                    elif a == c and d != b:
                        return False
                    else:
                        x = (d - b) / (a - c)
                        y = a * x + b
                        return Anchor(x, y)
                case Line(), Circle():
                    return chaos_math.find_line_intersect(obj.l2, obj.l1)
                case Circle(), Line():
                    return chaos_math.find_line_intersect(obj.l1, obj.l2)
                case Circle(), Circle():
                    return chaos_math.find_circle_intersect(obj.l1, obj.l2)
