import numpy as np
import cv2
from round import round_half_up

# 6m measurements
first6m = 6
second6m = 12
third6m = 18
fourth6m = 24
fifth6m = 30
sixth6m = 36

#BGR Color
c_green = (0, 255, 0)
c_red = (0, 0, 255)
# Thickness of -1 will fill the entire shape
thickness = -1
# Line thickness for text of 2 px
thickness = 2
# fontScale
fontScale = 0.8
# font
font = cv2.FONT_HERSHEY_SIMPLEX
    

def drawText(visual, height, middle, dist_to_car):

    # Define origin of the text
    org = (middle-170, height-10)
    
    # Needs to be inverted because OpenCV measures from top of the frame
    if dist_to_car > min_break_dist:
        visual = cv2.putText(visual, 'You are driving too close!', org, font, fontScale, c_red, thickness, cv2.LINE_AA)
    elif dist_to_car == 0:
        visual = cv2.putText(visual, 'No car detect!', org, font, fontScale, c_green, thickness, cv2.LINE_AA)
    else:
        visual = cv2.putText(visual, 'You are keeping enough space', org, font, fontScale, c_green, thickness, cv2.LINE_AA)
    
    return visual
    
# CURRENTLY NOT USED
def drawRectangle(visual, middle, x, dist_to_car):

    global min_break_dist
    # 4th degree poly for distance estimation
    min_break_dist = 0.0002*(x*x*x*x) - 0.0225*(x*x*x) + 0.9073*(x*x) - 16.7952*x + 480.2879
    min_break_dist = round_half_up(min_break_dist)
    
    # Start and End-point of the reactangle
    start_point = (middle-40, int(round_half_up(min_break_dist-1)))
    end_point = (middle+40, int(round_half_up(min_break_dist+1)))
    
    #DRAWING CAN BE ENABLED HERE
#    if dist_to_car > min_break_dist:
#        visual = cv2.rectangle(visual, start_point, end_point, c_red, thickness)
#    else:
#        visual = cv2.rectangle(visual, start_point, end_point, c_green, thickness)
    
    return visual
    
    
def draw_distance(visual, velocity, dist_to_car):
        
    height, width = visual.shape[:2]
        
    # middle of the frame
    middle = int(width/2)
    
    # break-distance in danger
    b_distance = int(((velocity/10) * (velocity/10)) / 2)
    print("Minimum Danger-Break_distance: " + str(b_distance))
    
    # Draw break-distance
    visual = drawRectangle(visual, middle, b_distance, dist_to_car)
    
    # Draw Altert Text
    visual = drawText(visual, height, middle, dist_to_car)

    return visual

# breakdistance in danger = ((velocity/10) * (velocity/10)) / 2
