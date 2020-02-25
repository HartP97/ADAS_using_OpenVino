import numpy as np
import cv2
from round import round_half_up

def region_of_interest(img, vertices, rect_vertices):
    # Define a blank matrix that matches the image height/width.
    mask = np.zeros_like(img)    # Retrieve the number of color channels of the image.
    channel_count = img.shape[2]    # Create a match color with the same color channel counts.
    match_mask_color = (255,) * channel_count
    
    # Fill inside the polygon
    cv2.fillPoly(mask, vertices, match_mask_color)
    cv2.fillPoly(mask, rect_vertices, match_mask_color)
    
    # Returning the image only where mask pixels match
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def cropImage(frame):
    
    # Get height of input image
    height, width = frame.shape[:2]
    # Define corners of triangle
    top = (int(round_half_up(width/2,0)), int(round_half_up(height/1.43, 0))) #height/1.47 1.43
    left = (0, int(round_half_up(height*0.9)))
    right = (width, int(round_half_up(height*0.9)))

    region_of_interest_vertices = [(left),(top),(right),]
    
    # Define corners of rectangle
    rect_top_left = (0, int(round_half_up(height*0.9)))
    rect_top_right = (width, int(round_half_up(height*0.9)))
    rect_bot_left = (0, height)
    rect_bot_right = (width, height)
    
    rect_of_interest_vertices = [(rect_top_left),(rect_top_right),(rect_bot_right),(rect_bot_left),]
    
    cropped_image = region_of_interest(frame, np.array([region_of_interest_vertices], np.int32), np.array([rect_of_interest_vertices], np.int32),)
    
    return cropped_image
