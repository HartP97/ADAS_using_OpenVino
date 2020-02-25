import cv2
import numpy as np
from round import round_half_up


def splitLeftRight(mask):

# Get height and width of mask
    height, width = mask.shape[:2]
    
# Black out left side to just receive right lines
    # represents the top left corner of rectangle
    start_right = (0, 0)
    # bottom right corner of rectangle
    end_right = (int(round_half_up(width/2)), height)
    
# Black out right side to just receive left lines
    start_left = (int(round_half_up(width/2)), 0)
    # bottom right corner of rectangle
    end_left = (width, height)
    
    # Black color in BGR
    color = (0, 0, 0)
    # Line thickness of -1 to fill rectangle
    thickness = -1

# Copy mask
    right_mask = mask.copy()
    left_mask = mask.copy()
# Apply black square
    right_mask = cv2.rectangle(right_mask, start_right, end_right, color, thickness)
    left_mask = cv2.rectangle(left_mask, start_left, end_left, color, thickness)
    
    return right_mask, left_mask
