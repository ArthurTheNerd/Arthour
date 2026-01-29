import pygame
import math
import os

# -----------------------------
# Initialization
# -----------------------------
os.environ['SDL_VIDEO_CENTERED'] = '1'
background, bright = (13, 13, 13), (60, 180, 120)
width, height = 800, 800

pygame.init()
pygame.display.set_caption('ASCII TESSERACT')
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60

# ASCII Fonts
lineFont = pygame.font.SysFont('scheherazade', 20, bold=False)
cornerFont = pygame.font.SysFont('nachlieliclm', 24, bold=True)

# Tesseract info
angle = 0
cube_position = [width//2, height//2]
scale = 2800
speed = 0.005

# 4D tesseract points
points = [
    [[-1], [-1], [1], [1]], [[1], [-1], [1], [1]],
    [[1], [1], [1], [1]], [[-1], [1], [1], [1]],
    [[-1], [-1], [-1], [1]], [[1], [-1], [-1], [1]],
    [[1], [1], [-1], [1]], [[-1], [1], [-1], [1]],
    [[-1], [-1], [1], [-1]], [[1], [-1], [1], [-1]],
    [[1], [1], [1], [-1]], [[-1], [1], [1], [-1]],
    [[-1], [-1], [-1], [-1]], [[1], [-1], [-1], [-1]],
    [[1], [1], [-1], [-1]], [[-1], [1], [-1], [-1]]
]

# -----------------------------
# Helper functions
# -----------------------------
def matrix_multiplication(a, b):
    """Multiply matrices a x b."""
    result = [[0] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b)):
            result[i][0] += a[i][j] * b[j][0]
    return result

def bresenham(x0, y0, x1, y1):
    """Return points on a line using Bresenham's algorithm."""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points

def interp(val, in_range, out_range):
    """Linear interpolation."""
    (a, b), (c, d) = in_range, out_range
    return c + (val - a) * (d - c) / (b - a)

def connect_point(i, j, k, offset, lineChar=':', skip=7):
    a = k[i + offset]
    b = k[j + offset]
    line = bresenham(a[0], a[1], b[0], b[1])
    s = skip
    for point in line:
        s -= 1
        if s == 0:
            text_display(lineChar, point[0], point[1])
        if s < 0:
            s = skip

def text_display(letter, x_pos, y_pos):
    text = lineFont.render(str(letter), True, bright)
    screen.blit(text, (x_pos, y_pos))

def corner_display(x, y, z, w, interpolateColor=True, fontSizeInterpolate=True):
    if interpolateColor:
        interpolatedColor = (
            int(interp(z, [0.1, 0.27], [background[0], bright[0]])),
            int(interp(z, [0.1, 0.27], [background[1], bright[1]])),
            int(interp(z, [0.1, 0.27], [background[2], bright[2]]))
        )
    else:
        interpolatedColor = bright

    if fontSizeInterpolate:
        fontSize = round(int(interp(w, [0.1, 0.27], [50, 76])))
        localFont = pygame.font.SysFont('nachlieliclm', fontSize, bold=True)
    else:
        localFont = cornerFont

    text = localFont.render('.', True, interpolatedColor)
    screen.blit(text, (x, y - fontSize / 2))

# -----------------------------
# Main loop
# -----------------------------
run = True
while run:
    clock.tick(fps)
    screen.fill(background)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            run = False

    index = 0
    projected_points = [0] * len(points)

    # 3D rotations
    rotation_x = [
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ]
    rotation_y = [
        [math.cos(angle), 0, -math.sin(angle)],
        [0, 1, 0],
        [math.sin(angle), 0, math.cos(angle)]
    ]
    rotation_z = [
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ]

    tesseract_rotation = [
        [1, 0, 0],
        [0, math.cos(-math.pi/2), -math.sin(-math.pi/2)],
        [0, math.sin(-math.pi/2), math.cos(-math.pi/2)]
    ]

    # 4D rotations
    rotation4d_xy = [
        [math.cos(angle), -math.sin(angle), 0, 0],
        [math.sin(angle), math.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    rotation4d_xz = [
        [math.cos(angle), 0, -math.sin(angle), 0],
        [0, 1, 0, 0],
        [math.sin(angle), 0, math.cos(angle), 0],
        [0, 0, 0, 1]
    ]
    rotation4d_xw = [
        [math.cos(angle), 0, 0, -math.sin(angle)],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [math.sin(angle), 0, 0, math.cos(angle)]
    ]
    rotation4d_yz = [
        [1, 0, 0, 0],
        [0, math.cos(angle), -math.sin(angle), 0],
        [0, math.sin(angle), math.cos(angle), 0],
        [0, 0, 0, 1]
    ]
    rotation4d_yw = [
        [1, 0, 0, 0],
        [0, math.cos(angle), 0, -math.sin(angle)],
        [0, 0, 1, 0],
        [0, math.sin(angle), 0, math.cos(angle)]
    ]
    rotation4d_zw = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, math.cos(angle), -math.sin(angle)],
        [0, 0, math.sin(angle), math.cos(angle)]
    ]

    # Project points
    for point in points:
        rotated_3d = matrix_multiplication(rotation4d_xy, point)
        rotated_3d = matrix_multiplication(rotation4d_zw, rotated_3d)

        distance = 5
        w = 1 / (distance - rotated_3d[3][0])
        projection_matrix4 = [
            [w, 0, 0, 0],
            [0, w, 0, 0],
            [0, 0, w, 0]
        ]
        projected_3d = matrix_multiplication(projection_matrix4, rotated_3d)
        rotated_2d = matrix_multiplication(tesseract_rotation, projected_3d)

        z = 1 / (distance - (rotated_2d[2][0] + rotated_3d[3][0]))
        projection_matrix = [[z, 0, 0], [0, z, 0]]

        rotated_2d = matrix_multiplication(rotation_x, projected_3d)
        projected_2d = matrix_multiplication(projection_matrix, rotated_2d)

        x = int(projected_2d[0][0] * scale) + cube_position[0]
        y = int(projected_2d[1][0] * scale) + cube_position[1]

        projected_points[index] = [x, y, z, w]
        corner_display(x, y, z, w)
        index += 1

    # Draw edges
    for m in range(4):
        connect_point(m, (m+1)%4, projected_points, 8)
        connect_point(m+4, (m+1)%4 + 4, projected_points, 8)
        connect_point(m, m+4, projected_points, 8)

    for m in range(4):
        connect_point(m, (m+1)%4, projected_points, 0)
        connect_point(m+4, (m+1)%4 + 4, projected_points, 0)
        connect_point(m, m+4, projected_points, 0)

    for m in range(8):
        connect_point(m, m+8, projected_points, 0)

    angle += speed
    pygame.display.update()

pygame.quit()
