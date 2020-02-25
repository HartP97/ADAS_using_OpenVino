import numpy as np
import cv2, math
from round import round_half_up
from split_mask import splitLeftRight

def truncList(list1, list2):
    len_list1 = len(list1)
    len_list2 = len(list2)
    
# IF list1 bigger list2, trunc values
    if len_list1 > len_list2:
        del list1[len_list2:]
    elif len_list2 > len_list1:
        diff = len_list2 - len_list1
        del list2[len_list1:]
    
    return list1, list2

# delete eveything but the first point of each y coordinate
def receiveInterestPoints(list):
    for i in range(len(list)):
        #-1 because list objects start at 0 and length at 1
        len_list = (len(list[i])) - 1
        # remove all but not 1 position
        while len_list > 0:
            list[i].pop(len_list)
            len_list = len_list - 1
    return list
    
# convert 3D to 2D list
def to2D(list):
    list2D = []
    for i in list:
        for j in i:
            list2D.append(j)
    return list2D
    
def sortLane(list_lane, list_value, list_sorted, list_3D):
    # iterate through left_lane until list end
    for i in range(len(list_lane)):

    # add to left_sorted if similar
        if list_lane[i][1] == list_value:
            list_sorted.append(list_lane[i])

    # else if y wert sich aendert packe left_sorted in left_3D und leere left_sorted
        elif list_lane[i][1] != list_value:
            list_3D.append(list_sorted)
            list_sorted = []

        list_value = list_lane[i][1]

    # Delete empty list objects
    list_3D = [x for x in list_3D if x != []]

    return list_lane, list_value, list_sorted, list_3D
