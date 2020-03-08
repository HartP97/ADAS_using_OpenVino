import cv2

# Text-Color
c_white = (255, 255, 255)
# Thickness of -1 will fill the entire shape
thickness = -1
# Line thickness for text of 2 px
thickness = 2
# fontScale
fontScale = 0.8
# font
font = cv2.FONT_HERSHEY_SIMPLEX

def print_weather(frame, visual, weather_text):
    
    height, width = visual.shape[:2]
    
    # Define origin of the text
    org = (width-120, 35)

    visual = cv2.putText(visual, weather_text, org, font, fontScale, c_white, thickness, cv2.LINE_AA)

    return visual
