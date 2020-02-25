import cv2
import numpy as np
from region_interest import cropImage
from split_mask import splitLeftRight
from listOperations import truncList
from listOperations import receiveInterestPoints
from listOperations import to2D
from listOperations import sortLane

# Decleration of global variables
global_lines = []
mask_list=[]
combined_mask = 0
counter = 0
kernel_comb = np.ones((3,3),np.uint8)
y1= 0
alpha = 0.3
left_value = 0
right_value = 0
left_sorted = []
right_sorted = []
left_3D = []
right_3D = []
final_3D = []
color = (0, 255, 0)
thickness = -1
#For trackSpeed()
fps = 30
# each white line has the length of 6m
line_length = 6
count_frames = 0

def trackSpeed(right_uncombined):

    global count_frames
    
    #get width and height
    height, width = right_uncombined.shape[:2]
    
    [y_coord_R, x_coord_R] = np.where(right_uncombined != [0])
    #####print(y_coord_R[-1])
    
    if y_coord_R[-1] == 479:
        count_frames += 1
    elif y_coord_R[-1] != 479 and count_frames != 0:
        # percentage of 1 second
        percentage_s = count_frames/fps
        # convert to milliseconds
        mil_seconds = percentage_s * 1000
        #meter/ms
        meter_per_mil_sec = line_length/mil_seconds
        #velocity in km/h
        velocity = meter_per_mil_sec * 3600
        count_frames = 0
        return velocity
    

def getSpeed(frame):
  
    # Crop frame to the region of interest (see region_interest file)
    frame_cropped =  cropImage(frame)

    # Convert Colorspace from BGR to HlS
    hls = cv2.cvtColor(frame_cropped, cv2.COLOR_BGR2HLS)

    # Define white color range (chose with trackbars before)
    lower_white = np.array([16, 120, 80])
    upper_white = np.array([21, 255, 255])
    maskW = cv2.inRange(hls, lower_white, upper_white)

    # Define yellow color range
    lower_yellow = np.array([0, 144, 0]) # lH, lL, lS
    upper_yellow = np.array([71, 234, 255]) # uH, uL, uS
    maskY = cv2.inRange(hls, lower_yellow, upper_yellow)
                
    # Combining both masks
    mask = maskW + maskY
           
    # Apply Closing on the mask
    kernel = np.ones((7,7),np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = closing

    right_uncombined, left_uncombined = splitLeftRight(mask)

    # Add mask of each frame to mask_list
    mask_list.append(mask)

    # If mask_list longer than 40, delete first mask
    if len(mask_list) > 40:
        mask_list.pop(0)

    # bitwise_or for those 40 masks to receive a continues filled line
    for mask in mask_list:
        global combined_mask
        combined_mask = cv2.bitwise_or(combined_mask, mask)
        combined_mask = cv2.dilate(combined_mask,kernel_comb,iterations = 4) #dilation = cv2.dilate(mask,...)
        combined_mask = cv2.erode(combined_mask,kernel_comb,iterations = 4)

    # Split combined_mask in left and right side (function can be found in split_mask.py)
    right_mask, left_mask = splitLeftRight(combined_mask)

    # Get coordinates for white pixel right side
    [y_coord_R, x_coord_R] = np.where(right_mask != [0])
    # Get coordinates for white pixel right side
    [y_coord_L, x_coord_L] = np.where(left_mask != [0])

    # Reset list variables each iteration so they can be freshly filled
    left_lane = []
    right_line = []
    left_value = 0
    right_value = 0
    left_sorted = []
    right_sorted = []
    left_3D = []
    right_3D = []
    final_3D = []

    # Combine each side to one 2D list
    right_lane = list(zip(x_coord_R, y_coord_R))
    left_lane = list(zip(x_coord_L, y_coord_L))

    # Sort list y smallest to biggest
    left_lane = sorted(left_lane,key=lambda l:l[1])
    right_lane = sorted(right_lane,key=lambda l:l[1])

    # Merge coordinates of left_lane with same y value together in left_3D
    # function can be found in listOperations.py
    left_lane, left_value, left_sorted, left_3D = sortLane(left_lane, left_value, left_sorted, left_3D)
    # Do the same for the right_lane
    right_lane, right_value, right_sorted, right_3D = sortLane(right_lane, right_value, right_sorted, right_3D)

    # Sorting left_3D by biggest x coordinates first
    # right_3D is already sorted the way we need it
    for i in range(len(left_3D)):
        left_3D[i].sort(reverse = True)

    # Delete all unnecessary values from each list, function can be found in listOperations.py
    left_3D = receiveInterestPoints(left_3D)
    right_3D = receiveInterestPoints(right_3D)

    # Convert the now unnecessary 3D structed lists to a 2D structure
    left_2D = to2D(left_3D)
    right_2D = to2D(right_3D)

    # Find matches in left_3D and right_3D and put them together in final_3D
    for i in range(len(left_2D)):
        for j in range(len(right_2D)):
            if left_2D[i][1] == right_2D[j][1]:
                tempList = []
                tempList.append(left_2D[i])
                tempList.append(right_2D[j])
                final_3D.append(tempList)
                tempList = []
                
    # Create copies of frame for output with lane detection overlay
    overlay = frame.copy()
    output = frame.copy()

    # If not empty connect matching points and draw
    if len(final_3D) != 0:
        for i in range(len(final_3D)):
            start_point = final_3D[i][0]
            end_point = final_3D[i][1]
            # Draw rectangle/line
            overlay = cv2.rectangle(overlay, start_point, end_point, color, thickness)
           
    # Apply the overlay onto the output
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    # Combine frame and combined mask (just for visual output)
    result = cv2.bitwise_and(frame, frame, mask=combined_mask)

    # calculate Speed inside trackSpeed
    velocity = trackSpeed(right_uncombined)

    # Set combined_mask to 0 again
    combined_mask = 0

    return velocity
