import numpy as np
from pathlib import Path
import ctypes

# Load the shared library
lib = ctypes.CDLL(str(Path(__file__).parent / "library.so"))
# Define the function signature
lib.does_line_intersect_square.restype = ctypes.c_int
lib.does_line_intersect_square.argtypes = (
ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float)



def is_line_inside(k: float, b: float, x_q: float, y_q: float, d: float) -> bool:
    """
    Check if a line defined by the equation y = kx + b is inside a square with side length d,
    centered at the point (x_q, y_q).

    Args:
        k (float): The slope of the line.
        b (float): The y-intercept of the line.
        x_q (float): The x-coordinate of the center of the square.
        y_q (float): The y-coordinate of the center of the square.
        d (float): The diagonal length of the square.

    Returns:
        bool: True if the line is inside the square, False otherwise.
    """
    s =  d/np.sqrt(2)
    x1, y1 = x_q - s/2, y_q - s/2
    x2, y2 = x_q + s/2, y_q + s/2
    return bool(lib.does_line_intersect_square(k, b, x1, y1, x2, y2))


def does_line_intersect_square(k, b, x1, y1, x2, y2):

    # Вычисляем y для x-координат квадрата
    y_at_x1 = k * x1 + b
    y_at_x2 = k * x2 + b

    # Если y для какой-либо x-координаты квадрата лежит внутри y-координат квадрата, то прямая пересекает квадрат
    if y1 <= y_at_x1 < y2 or y1 < y_at_x2 <= y2:
        return True

    # Вычисляем x для y-координат квадрата
    x_at_y1 = (y1 - b) / k
    x_at_y2 = (y2 - b) / k

    # Если x для какой-либо y-координаты квадрата лежит внутри x-координат квадрата, то прямая пересекает квадрат
    if x1 <= x_at_y1 < x2 or x1 < x_at_y2 <= x2:
        return True

    return False



def make_quadro_corners(hor_side_c, vert_side_c, side):
    d = np.sqrt(
        2 * np.power(side, 2)
    )
    poly_attrs = np.zeros(
        shape=(vert_side_c, hor_side_c, 2), dtype=float,
    )

    for ver_pos in range(vert_side_c):
        y_min = ver_pos * side
        y_max = (ver_pos + 1) * side
        for hor_pos in range(hor_side_c):
            x_min = hor_pos * side
            x_max = (hor_pos + 1) * side
            poly_attrs[ver_pos][hor_pos] = np.array(
                [(x_max + x_min) / 2, (y_max + y_min) / 2]
            )
    return poly_attrs, d


def gen_quadro_poly_start_points(hor_side_c, vert_side_c, side: float):
    for hor_n in range(hor_side_c):
        y_min = side * hor_n
        for vert_n in range(vert_side_c):
            x_min = side * vert_n
            yield y_min, x_min
