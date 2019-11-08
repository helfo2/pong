from math import *
from random import *
from config import *

BOUNCE_ANGLE = radians(75)

LEFT_WINDOW_TOP = [0, 0]
LEFT_WINDOW_BOTTOM = [0, WINDOW_HEIGHT]

RIGHT_WINDOW_TOP = [WINDOW_WIDTH, 0]
RIGHT_WINDOW_BOTTOM = [WINDOW_WIDTH, WINDOW_HEIGHT]

def get_segment_intersection(p1_x, p1_y, p2_x, p2_y, q1_x, q1_y, q2_x, q2_y):
    """ Returns point if the lines intersect, otherwise 0. Based on cross product

    t = (q-p) x s / (r x s)
    u = (q-p) x r / (r x s)

    https://www.youtube.com/watch?v=c065KoXooSw
    """

    r_x = p2_x - p1_x
    r_y = p2_y - p1_y
    
    s_x = q2_x - q1_x
    s_y = q2_y - q1_y

    cross_prod = -s_x * r_y + r_x * s_y
    if cross_prod == 0: # collinear
        return None

    s = ( r_x * (p1_y - q1_y) - r_y * (p1_x - q1_x) ) / cross_prod
    t = ( s_x * (p1_y - q1_y) - s_y * (p1_x - q1_x) ) / cross_prod

    if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
        # collision detected
        i_x = p1_x + (t * r_x)
        i_y = p1_y + (t * r_y)
        
        return [i_x, i_y]


    return None # no collision


def on_segment(p, q, r):
    """ If point q lies on segment pr """
    return q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])


def orientation(p, q, r):
    """ Finds orientation of ordered triplet (p, q, r) 
        Returns:
            0: all points are colinear
            1: clockwise
            2: counterclockwise
    """
    # use the slope to get orientation
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if val == 0: # colinear
        return 0

    return 1 if val > 0 else 2 # clock or counterclokwise
 

def do_intersect(p1, q1, p2, q2):
    """ Returns if segments p1q1 and p2q2 intersect """
    # first finds orientations
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # general case
    if o1 != o2 and o3 != o4:
        return True

    # p1, q1 and p2 colinear and p2 on p1q1
    if o1 == 0 and on_segment(p1, p2, q1):
        return True

    # p1, q1 and q2 colinear and q2 on p1q1
    if o2 == 0 and on_segment(p1, q2, q1):
        return True

    # p2, q2 and p1 colinear and q1 on p2q2
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
  
    # p2, q2 and q1 colinear and q1 on p2q2
    if o4 == 0 and on_segment(p2, q1, q2):
        return True
  
    return False


def interpolate(value, start, end, new_start, new_end):
    return new_start + (new_end - new_start) * ((value - start) / (end - start))


def create_line(point_a, point_b):
    """ encapsulates a segment from point_a.x, point_a.y to point_b.x, point_b.y """
    return [point_a, point_b]
