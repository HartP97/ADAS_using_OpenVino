import argparse
import cv2
from inference import Network
from region_interest import cropImage
import numpy as np
from traffic_sign import draw_sign
from drawCars import draw_cars
from distance import draw_distance
from speed import getSpeed

local_velocity = 0
icon = cv2.imread("car.png")
sign = cv2.imread("sign.png")
#Icons made by "Nikita Golubev" "https://www.flaticon.com/authors/nikita-golubev" from https://www.flaticon.com/"
INPUT_STREAM = "input_vid.mp4"
CPU_EXTENSION = "/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension.dylib"

def get_args():
    '''
    Gets the arguments from the command line.
    '''
    parser = argparse.ArgumentParser("Run inference on an input video")
    # -- Create the descriptions for the commands
    m_desc = "The location of the model XML file"
    i_desc = "The location of the input file"
    d_desc = "The device name, if not 'CPU'"
    c_desc = "The color of the bounding boxes to draw; RED, GREEN or BLUE"
    ct_desc = "The confidence threshold to use with the bounding boxes"

    # -- Add required and optional groups
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # -- Create the arguments
    required.add_argument("-m", help=m_desc, required=True)
    optional.add_argument("-i", help=i_desc, default=INPUT_STREAM)
    optional.add_argument("-d", help=d_desc, default='CPU')
    optional.add_argument("-c", help=c_desc, default='BLUE')
    optional.add_argument("-ct", help=ct_desc, default=0.5)
    args = parser.parse_args()

    return args

def convert_color(color_string):
    '''
    Get the BGR value of the desired bounding box color.
    Defaults to Blue if an invalid color is given.
    '''
    colors = {"BLUE": (255,0,0), "GREEN": (0,255,0), "RED": (0,0,255)}
    out_color = colors.get(color_string)
    if out_color:
        return out_color
    else:
        return colors['BLUE']

def infer_on_video(args):
    # Converting arguments for color and confidence
    args.c = convert_color(args.c)
    args.ct = float(args.ct)
    
    ### TODO: Initialize the Inference Engine
    plugin = Network()

    ### TODO: Load the network model into the IE
    plugin.load_model(args.m, args.d, CPU_EXTENSION)
    net_input_shape = plugin.get_input_shape()

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

        ### Pre-process the frame
        p_frame = cv2.resize(frame, (net_input_shape[3], net_input_shape[2]))
        p_frame = p_frame.transpose((2,0,1))
        p_frame = p_frame.reshape(1, *p_frame.shape)

        ### Perform inference on the frame
        plugin.async_inference(p_frame)
        
        ### Get the output of inference
        if plugin.wait() == 0:
            result = plugin.extract_output()
            ### TODO: Update the frame to include detected bounding boxes
            
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
            
            ##### ADD FUNCTIONS USING MODELS HERE (START) #####
            
            '''
            HINT: Maybe we can implement them like I did with the above
            draw_cars() which then addresses the inference engine from
            another file, to keep it organized
            '''
            
            ##### ADD FUNCTIONS USING MODELS HERE (END) #####
            
            # Add traffic sign to visual
            visual = draw_sign(frame, visual, sign)
            
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

#source /opt/intel/openvino/bin/setupvars.sh
