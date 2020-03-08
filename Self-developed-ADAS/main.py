import argparse
import cv2
from inference import Network
from region_interest import cropImage
import numpy as np
from traffic_sign import draw_sign
from drawCars import draw_cars
from distance import draw_distance
from speed import getSpeed
from weather import print_weather

local_velocity = 0
icon = cv2.imread("car.png")
sign = cv2.imread("sign.png")
CAR_MODEL = "models/frozen_inference_graph.xml"
WEATHER_MODEL = "models/onnx_weather.xml"
WEATHER_TYPES=['Snow','Rainy','Sunny','Haze','Cloudy','Thunder']
#Icons made by "Nikita Golubev" "https://www.flaticon.com/authors/nikita-golubev" from https://www.flaticon.com/"
INPUT_STREAM = "input_vid.mp4"
CPU_EXTENSION = "/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension.dylib"

def get_args():
    '''
    Gets the arguments from the command line.
    '''
    parser = argparse.ArgumentParser("Run inference on an input video")
    # -- Create the descriptions for the commands
    i_desc = "The location of the input file"
    d_desc = "The device name, if not 'CPU'"
    ct_desc = "The confidence threshold to use with the bounding boxes"

    # -- Add required and optional groups
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # -- Create the arguments
    optional.add_argument("-i", help=i_desc, default=INPUT_STREAM)
    optional.add_argument("-d", help=d_desc, default='CPU')
    optional.add_argument("-ct", help=ct_desc, default=0.5)
    args = parser.parse_args()

    return args

def infer_on_video(args):
    # Converting arguments for color and confidence
    args.ct = float(args.ct)
    
    ### Initialize the Inference Engine
    plugin_car = Network()
    plugin_weather = Network()

    ### Load the network car-model into the IE
    plugin_car.load_model(CAR_MODEL, args.d, CPU_EXTENSION)
    ### Load the network wheather-model into the IE
    plugin_weather.load_model(WEATHER_MODEL, args.d, CPU_EXTENSION)
    
    ### Get net_input_shape for car and weather model
    net_input_shape_car = plugin_car.get_input_shape()
    net_input_shape_weather = plugin_weather.get_input_shape()

    # Get and open video capture
    cap = cv2.VideoCapture(args.i)
    cap.open(args.i)

    # Grab the shape of the input 
    width = int(cap.get(3))
    height = int(cap.get(4))

    # Create a video writer for the output video
    # The second argument should be `cv2.VideoWriter_fourcc('M','J','P','G')`
    # on Mac, and `0x00000021` on Linux
    #out = cv2.VideoWriter('out3.mp4', 0x00000021, 30, (width,height))
    
    # Process frames until the video ends, or process is exited
    while cap.isOpened():
        # Read the next frame
        flag, frame = cap.read()
        if not flag:
            break
        key_pressed = cv2.waitKey(60)

        ### Pre-process the frame for car
        p_frame_car = cv2.resize(frame, (net_input_shape_car[3], net_input_shape_car[2]))
        p_frame_car = p_frame_car.transpose((2,0,1))
        p_frame_car = p_frame_car.reshape(1, *p_frame_car.shape)
        
        ### Pre-process the frame for car
        p_frame_weather = cv2.resize(frame, (255, 255))
        p_frame_weather = p_frame_weather.transpose((2,0,1))
        p_frame_weather = p_frame_weather.reshape(1, 3, 255, 255)

        ### Perform inference on the frame for car
        plugin_car.async_inference(p_frame_car)
        plugin_weather.async_inference(p_frame_weather)
        
        ### Get the output of inference
        if plugin_car.wait() == 0 and plugin_weather.wait() == 0:
            ### Get results for car and weather
            result = plugin_car.extract_output()
            weather_output = plugin_weather.extract_output_weather()
            ### Get highest value of weather_output
            weather_pred = np.argmax(weather_output['1168'].flatten())
            ### Get text for highest value
            weather_text = WEATHER_TYPES[weather_pred]
            print("Weather_text: " + str(weather_text))
            
            ### Update the frame to include detected bounding boxes
            visual = frame.copy()
            copied_frame = frame.copy()
            # Crop frame to the region of interest (see region_interest file)
            visual_cropped = cropImage(visual)
            
            # Convert Colorspace from BGR to HlS
            hls = cv2.cvtColor(visual_cropped, cv2.COLOR_BGR2HLS)

            # Define yellow color range for lane-lines (e.g. for US-roads)
            lower_yellow = np.array([16, 120, 80])
            upper_yellow = np.array([21, 255, 255])
            maskY = cv2.inRange(hls, lower_yellow, upper_yellow)

            # Define white color range for lane-line
            lower_white = np.array([0, 144, 0])  # lH, lL, lS
            upper_white = np.array([71, 234, 255])  # uH, uL, uS
            maskW = cv2.inRange(hls, lower_white, upper_white)

            # Combining both masks
            mask = maskW + maskY
        
            # Apply Closing on the mask
            kernel = np.ones((7, 7), np.uint8)
            visual = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            visual = np.stack((visual,)*3, axis=-1)
            
            # Add cars to visual
            visual, dist_to_car = draw_cars(visual, result, args, width, height, icon)
            
            # Add traffic sign to visual
            visual = draw_sign(frame, visual, sign)
            
            # Add Weather text
            visual = print_weather(frame, visual, weather_text)
            
            # Get speed of the car
            velocity = getSpeed(frame)
            global local_velocity
            
            if velocity != None:
                local_velocity = velocity
            else:
                pass
                
            # Add distance to visual
            visual = draw_distance(visual, local_velocity, dist_to_car)
            
            # Write out the frame
            #out.write(frame)
            cv2.imshow("Visual Output", visual)
            cv2.imshow("Orig", frame)
        # Break if escape key pressed
        if key_pressed == 27:
            break

    # Release the out writer, capture, and destroy any OpenCV windows
    #out.release()
    cap.release()
    cv2.destroyAllWindows()

def main():
    args = get_args()
    infer_on_video(args)


if __name__ == "__main__":
    main()
'''
source /opt/intel/openvino/bin/setupvars.sh
'''
