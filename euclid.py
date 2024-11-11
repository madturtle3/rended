import pygame
from euclib import *

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
window = pygame.display.set_mode((500, 500))
window.fill(WHITE)


def rtop(p: Anchor):
    return window.get_width() / 2 * (p.x + 1), -window.get_height() / 2 * (p.y - 1)


# pyagme draw it
def draw(*args: list[Point | Line | Circle]):
    for obj in args:
        match obj:
            # our concrete case
            case Anchor():
                # pygame to real this
                print("drawing anchor", obj)
                pygame.draw.circle(window, (125,75,125), rtop(obj), 5)
            case Intersect():
                for pt in get_location(obj):
                    print()
                    draw(pt)
            case Circle():
                anchor_center = get_location(obj.center)
                pygame.draw.circle(
                    window,
                    BLACK,
                    rtop(anchor_center),
                    obj.radius * window.get_width() / 2,
                    1,
                )


if __name__ == "__main__":
    # create our four fundamental anchors
    top_left = Anchor(-1, 1)
    top_right = Anchor(1, 1)
    bottom_left = Anchor(-1, -1)
    bottom_right = Anchor(1, -1)
    # go crazy and draw here
    c1 = Circle(top_left, 2)
    c2 = Circle(top_right, 2)
    between_points = Intersect(c1, c2)
    draw(c1,c2,between_points)
    pygame.display.flip()
    input()
