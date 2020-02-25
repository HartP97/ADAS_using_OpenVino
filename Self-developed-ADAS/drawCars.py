import cv2

def draw_cars(visual, result, args, width, height, icon):

    # Get boudning boxes measurements
    for box in result[0][0]:
        conf = box[2]
        if conf >= args.ct:
            xmin = int(box[3] * width)
            ymin = int(box[4] * height)
            xmax = int(box[5] * width)
            ymax = int(box[6] * height)
       
        
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
                
    return visual, ymax
