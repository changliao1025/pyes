import numpy as np
def calculate_hexagon_area(effe_edge):
    """
    Calculate the area of a hexagon grid
    """
    area = 1.5 * np.sqrt(3.0) * effe_edge
    return area