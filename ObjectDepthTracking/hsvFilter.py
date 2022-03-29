import sys
import cv2
import numpy as np
import time

def add_HSV_filter(frame):
    # Define a 5x5 kernel for erosion and dilation
    kernel = np.ones((5, 5), np.uint8)

	# Blurring the frame
    blur = cv2.GaussianBlur(frame,(5,5),0) 
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Define the upper and lower boundaries for a color to be considered "Blue"
    blueLower = np.array([100, 60, 60])
    blueUpper = np.array([140, 255, 255])    

    blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    blueMask = cv2.erode(blueMask, kernel, iterations=2)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(blueMask, kernel, iterations=1)

    return mask