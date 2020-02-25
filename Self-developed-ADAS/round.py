import cv2
import numpy as np
import math

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier
    
#    >>> round_half_up(1.23, 1)
#    1.2
#    >>> round_half_up(1.28, 1)
#    1.3
#    >>> round_half_up(1.25, 1)
#    1.3
#    >>> round_half_up(-1.5)
#    -1.0
#    >>> round_half_up(-1.25, 1)
#    -1.2
#    >>> round_half_up(2.5)
#    3.0
#    >>> round_half_up(-1.225, 2)
#    -1.23

def round_half_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n*multiplier - 0.5) / multiplier
    
#    >>> round_half_down(1.5)
#    1.0
#    >>> round_half_down(-1.5)
#    -2.0
#    >>> round_half_down(2.25, 1)
#    2.2
    
def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier
    
#    >>> round_up(1.1)
#    2.0
#    >>> round_up(1.23, 1)
#    1.3
#    >>> round_up(1.543, 2)
#    1.55
#    >>> round_up(22.45, -1)
#    30.0
#    >>> round_up(1352, -2)
#    1400
#     >>> round_up(-1.5)
#     -1.0

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier
    
#    >>> round_down(1.5)
#    1
#    >>> round_down(1.37, 1)
#    1.3
#    >>> round_down(-0.5)
#    -1
    
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier
    
#    >>> truncate(12.5)
#    12.0
#    >>> truncate(-5.963, 1)
#    -5.9
#    >>> truncate(1.625, 2)
#    1.62
#     >>> truncate(125.6, -1)
#     120.0
#     >>> truncate(-1374.25, -3)
#     -1000.0

# Rounding functions used from the following website:
# https://realpython.com/python-rounding/
