import os
import sys
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
#import tensorflow as tf

# Functions
import hsvFilter as hsv
import targetShape as shape
import findDepth as zdep

########################### CAMERA SETTINGS ################################################
# open webcam
cap = cv2.VideoCapture(1200) 
width = int(cap.get(3))
height = int(cap.get(4))
size = (width, height)

# Stereo camera settings
frame_rate = 60    #Camera frame rate (maximum at 60 fps)
B = 6               #Distance between the cameras [cm]
f = 3.6              #Camera lense's focal length [mm]
alpha = 100        #Camera field of view in the horisontal plane [degrees]

# Empty lists to store object detection spatial coordinates
X = []
Y = []
Z = []
##############################################################################################

fourcc = cv2.VideoWriter_fourcc(*'MPEG')
out = cv2.VideoWriter('RealTime/output_images/out.avi', fourcc, frame_rate, (width,height))

while(True):
    
    ret, frame = cap.read()

    # Split stereo camera to left and right frames
    fullFrame = frame.reshape([height, width, 3])
    leftFrame = fullFrame[:,:width//2]
    rightFrame = fullFrame[:,width//2:]

    # If cannot catch any frame, break
    if ret==False:                    
        break

    else:
        # Apply HSV mask filter
        # HSV file select color to detect
        mask_right = hsv.add_HSV_filter(rightFrame)
        mask_left = hsv.add_HSV_filter(leftFrame)

        # Result-frames after applying HSV-filter mask
        res_right = cv2.bitwise_and(rightFrame, rightFrame, mask=mask_right)
        res_left = cv2.bitwise_and(leftFrame, leftFrame, mask=mask_left) 

        # APPLYING SHAPE RECOGNITION:
        circles_right = shape.find_circles(rightFrame, mask_right)
        circles_left  = shape.find_circles(leftFrame, mask_left)

        # Hough Transforms can be used aswell or some neural network to do object detection
        ################## CALCULATING BALL DEPTH #########################################################

        # If no ball can be caught in one camera show text "TRACKING LOST"
        if np.all(circles_right) == None or np.all(circles_left) == None:
            cv2.putText(rightFrame, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
            cv2.putText(leftFrame, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)

        else:
            # Function to calculate depth of object. Outputs vector of all depths in case of several balls.
            # All formulas used to find depth is in video presentaion
            depth = zdep.find_depth(circles_right, circles_left, rightFrame, leftFrame, B, f, alpha)
            coor = np.asarray(circles_right)
            X.append(coor[0])
            Y.append(coor[1])
            z = np.round(depth, 2)
            Z.append(depth)
                       
            cv2.putText(rightFrame, "TRACKING", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0),2)
            cv2.putText(leftFrame, "TRACKING", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0),2)
            cv2.putText(rightFrame, "Distance: " + str(round(depth,3)), (200,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0),2)
            cv2.putText(leftFrame, "Distance: " + str(round(depth,3)), (200,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0),2)
            
        ##############################################################################################
        # Show the frames
        
        #cv2.imshow("mask left", mask_left)
        #cv2.imshow("mask right", mask_right) 
        cv2.imshow("frame left", leftFrame)
        cv2.imshow("frame right", rightFrame) 
        cv2.imshow('original', frame)
        out.write(frame)                
        # Hit "q" to close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release and destroy all windows before termination
cap.release()
out.release()
cv2.destroyAllWindows()

################################## SAVE COORDINATES ############################################################
xx, yy, zz = np.meshgrid(X,Y,Z)
print(f'Shape of xx: {xx.shape}\nShape of yy: {yy.shape}\nShape of zz: {zz.shape}\n')
np.savetxt('RealTime/spatial_loc/XX.txt', X)
np.savetxt('RealTime/spatial_loc/YY.txt', Y)
np.savetxt('RealTime/spatial_loc/ZZ.txt', Z)
