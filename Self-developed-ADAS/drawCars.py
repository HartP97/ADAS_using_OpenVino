import cv2

dist_to_car = 0

def draw_cars(visual, result, args, width, height, icon):

    # Get boudning boxes measurements
    for box in result[0][0]:
        conf = box[2]
        if conf >= args.ct:
            xmin = int(box[3] * width)
            ymin = int(box[4] * height)
            xmax = int(box[5] * width)
            ymax = int(box[6] * height)
            
            width_car = xmax - xmin
            mid_car = xmin + width_car/2
            
            # Only conider cars in front of you, which means close to the middle of the frame
            if mid_car >= 198 and mid_car <= 298:
                global dist_to_car
                dist_to_car = ymax
       
            if ymin>0 and xmin>0:
                # adjust icon dim proportional to bounding box
                height_icon = int(ymax - ymin)
                width_icon = int(xmax - xmin)
                dim = (width_icon, height_icon)
            
                # resize icon
                if (xmin+width_icon) < width:
                    icon_rez = cv2.resize(icon, dim, interpolation = cv2.INTER_AREA)
            
                    # put icon on top of frame
                    visual[ymin:ymin+icon_rez.shape[0], xmin:xmin+icon_rez.shape[1]] = icon_rez
                
    return visual, dist_to_car
