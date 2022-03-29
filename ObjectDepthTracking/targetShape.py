import sys
import cv2
import numpy as np

import time
#import imutils

def find_circles(frame, mask):
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # Only proceed if at least one contour was found
    if len(contours) > 0:
        # Sort the contours and find the largest one -- we
        # will assume this contour correspondes to the area of the bottle cap
        cnt = sorted(contours, key = cv2.contourArea, reverse = True)[0]

        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)

        # Get the moments to calculate the center of the contour (in this case Circle)
        M = cv2.moments(cnt)       #Finds center point
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Only proceed if the radius is greater than a minimum value
        if radius > 5:
            # Draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 0), -1)

        if radius < 20:
            pass

    return center