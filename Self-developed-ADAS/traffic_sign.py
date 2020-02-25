import numpy as np
import cv2

cnt = None
FONT = cv2.FONT_HERSHEY_SIMPLEX
COLOR = (255, 255, 255)
THICKNESS = 1
    
def draw_sign(frame, visual, sign):
# Convert Colorspace from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
    lower_blue = np.array([106, 131, 0]) # lH, lS, lV
    upper_blue = np.array([126, 255, 255]) # uH, uS, uV
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    ##### get only biggest blob in image #####
    # Generate intermediate image; use morphological closing to keep parts of the brain together
    inter = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    
    # Count white pixels of mask NUEVO
    white_px = np.sum(mask == 255)
    
    # Find largest contour in intermediate image only if there are white pixels in mask
    # otheriwse it crashes NUEVO
    if white_px != 0:
        cnts, _ = cv2.findContours(inter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnt = max(cnts, key=cv2.contourArea)
    ##### get biggest blob only #####
    
        # Output
        closed = np.zeros(mask.shape, np.uint8)
        #only if there are white pixels in mask otherwise it crashes NUEVO

        cv2.drawContours(closed, [cnt], -1, 255, cv2.FILLED)
        closed = cv2.bitwise_and(mask, closed)
        
        # Dilation and Erosion
        mkernel = np.ones((5,5),np.uint8)
        dilation = cv2.dilate(closed,mkernel,iterations = 5)
        erosion = cv2.erode(dilation,mkernel,iterations = 5)
        mask = erosion
    
        # Get coordinates for white pixel right side
        [y_coord_R, x_coord_R] = np.where(mask != [0])
    
        sign_coord = list(zip(x_coord_R, y_coord_R))
        # Sort list smallest to biggest
        sign_coord_y = sorted(sign_coord, key=lambda l: l[1])
        sign_coord_x = sorted(sign_coord, key=lambda l: l[0])
    
        #extract smallest x value only
        sign_xmin = sign_coord_x[0][0]
        #extract biggest x value only
        sign_xmax = sign_coord_x[-1][0]
        # calculate sign_width SHOULD BE HEIGHT but works like this
        sign_width = sign_xmax - sign_xmin
    
        #extract smallest y value only
        sign_ymin = sign_coord_y[0][1]
        #extract biggest y value only
        sign_ymax = sign_coord_y[-1][1]
        #calculate sign_height SHOULD BE WIDTH but works like this
        sign_height = sign_ymax - sign_ymin
    
        height, width = frame.shape[:2]
    
        # adjust icon dim proportional to detected area
        sign_dim = (220, 120)
    
        cropped = frame[sign_ymin:sign_ymax, sign_xmin:sign_xmax]
        
        # resize sign
        if (sign_xmin+sign_width) < width and sign_width > 0 and sign_height > 0:
        # Add cutout for sign to visual
            visual[sign_ymin:sign_ymin+cropped.shape[0], sign_xmin:sign_xmin+cropped.shape[1]] = cropped
    return visual
