# for now, just try to render a simple cube, don't worry about overlapping lines or anything
import pygame
import numpy

# I am NOT in the mood for float rounding chaos today!!!!
from decimal import Decimal
import dataclasses
import math
from math import pi

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

yaw_matrix = lambda yaw: numpy.array(
    [
        [math.cos(yaw), 0, -math.sin(yaw)],
        [0, 1, 0],
        [math.sin(yaw), 0, math.cos(yaw)],
    ]
)
pitch_matrix = lambda pitch: numpy.array(
    [
        [1, 0, 0],
        [0, math.cos(pitch), math.sin(pitch)],
        [0, -math.sin(pitch), math.cos(pitch)],
    ]
)


def ptoc(p, i=numpy.array(([1], [0], [0]))):
    r, yaw, pitch = p
    # construct the rotation matrix
    # yaw is Y axis rotation,
    # pitch is X axis rotation.
    # apply yaw first.
    scalar_matrix = numpy.identity(3) * r
    return pitch_matrix(pitch) @ yaw_matrix(yaw) @ scalar_matrix @ i


def rtop(p):
    # pygame to real
    x = p[0]
    y = p[1]
    return numpy.array((x + (window.get_width() / 2), -y + (window.get_height() / 2)))


def ptor(p):
    # real to pygame
    x = p[0]
    y = p[1]
    return numpy.array((x - (window.get_width() / 2), -y - (window.get_height() / 2)))


def distance(point: numpy.ndarray):
    return numpy.sum(numpy.sqrt(point))


@dataclasses.dataclass
class Camera:
    location: numpy.ndarray = dataclasses.field(
        default_factory=lambda: numpy.array((0, 0, 0))
    )
    yaw: float = 0
    pitch: float = 0
    """The idea for view_factor is that
    you will be able to do perspective with it"""
    fov: float = 4

    def move_direction(self, addend: numpy.ndarray):
        # rotate addend to align with our vector
        self.location += yaw_matrix(-self.yaw) @ pitch_matrix(-self.pitch) @ (addend)


def project_point(point: numpy.ndarray, camera: Camera):
    x, y, z = ptoc((1, camera.yaw, camera.pitch), (point - camera.location).T)
    projected = numpy.array((x, y), dtype=numpy.float64)
    distance = numpy.linalg.norm((x,y,z))
    if z>0:
        projected *= cam.fov/z
    else:
        projected = None
    return projected


def draw_polygon(
    polygon: numpy.ndarray,
    linelist: set[tuple[int, int]],
    camera=Camera(numpy.array((0, 0, 0))),
):
    # draw shape with Z axis truncated for now
    newpoints = []
    for point in polygon:
        newpoints.append(project_point(point, camera))
        color = (int(point[2] * 120), 0, 0)
        if type(newpoints[-1]) == numpy.ndarray:
            pygame.draw.circle(window, color, rtop(newpoints[-1] * 150), 5)
    for i1, p1 in enumerate(newpoints):
        for i2, p2 in enumerate(newpoints):
            if (i1, i2) in linelist:
                if type(p1) == numpy.ndarray and type(p2) == numpy.ndarray:
                    pygame.draw.line(window, BLACK, rtop(p1 * 150), rtop(p2 * 150))
    pygame.draw.circle(window, (200, 125, 0), rtop((0, 0)), 5)
    return newpoints


pygame.init()

RECT_POINTS = numpy.array(
    (
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 1),
        (1, 1, 1),
        (1, 1, 0),
        (1, 0, 0),
        (1, 0, 1),
        (0, 1, 0),
    )
)
LINE_SET: set = set()
for i1, p1 in enumerate(RECT_POINTS):
    for i2, p2 in enumerate(RECT_POINTS):
        same = 0
        for i in range(3):
            if p1[i] == p2[i]:
                same += 1
        if same >= 2:
            LINE_SET.add((i1, i2))

window = pygame.display.set_mode((500, 500))
cam = Camera(numpy.array((0.5, 0.5, -1)), 0, 0)
redraw = True
keys = set()
incval = 0.005
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.KEYDOWN:
            keys.add(event.key)
        elif event.type == pygame.KEYUP:
            keys.remove(event.key)
    for key in keys:
        redraw = True
        match key:
            case pygame.K_DOWN:
                cam.pitch += incval
            case pygame.K_UP:
                cam.pitch -= incval
            case pygame.K_LEFT:
                cam.yaw -= incval
            case pygame.K_RIGHT:
                cam.yaw += incval
            case pygame.K_e:
                cam.move_direction(numpy.array((0, incval, 0)))
            case pygame.K_q:
                cam.move_direction(numpy.array((0, -incval, 0)))
            case pygame.K_w:
                cam.move_direction(numpy.array((0, 0, incval)))
            case pygame.K_s:
                cam.move_direction(numpy.array((0, 0, -incval)))
            case pygame.K_a:
                cam.move_direction(numpy.array((-incval, 0, 0)))
            case pygame.K_d:
                cam.move_direction(numpy.array((incval, 0, 0)))
            case pygame.K_r:
                cam = Camera(numpy.array((0.5, 0.5, -incval)), 0, 0)
            case pygame.K_p:
                print(cam)

    if redraw:
        window.fill((255, 255, 255))
        result = draw_polygon(RECT_POINTS, LINE_SET, cam)
        pygame.display.flip()
        redraw = False
