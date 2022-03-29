import os
import time
import matplotlib
import numpy as np
from numpy import loadtxt
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

start_time = time.time()

# Space Coordinate
x = loadtxt('RealTime/spatial_loc/XX.txt')
y = loadtxt('RealTime/spatial_loc/YY.txt')
z = loadtxt('RealTime/spatial_loc/ZZ.txt')
t = np.linspace(start=0, stop=len(x), num=len(x))

# Setting up Data Set for Animation
dataSet = np.array([x, y, z])  # Combining our position coordinates
numDataPoints = len(x)

def animate_func(num):
    ax.clear()  # Clears the figure to update the line, point, title
    
    # Updating Trajectory Line (num+1 due to Python indexing)
    ax.plot3D(dataSet[0, :num+1], dataSet[1, :num+1], dataSet[2, :num+1], marker='o')

    # Updating Point Location 
    ax.scatter(dataSet[0, num], dataSet[1, num], dataSet[2, num], c='blue', marker='o')
    
    # Adding Constant Origin
    ax.plot3D(dataSet[0, 0], dataSet[1, 0], dataSet[2, 0], c='red', marker='o')
    ax.view_init(elev=25., azim=1*num)
       
    # Setting Axes Limits
    ax.set_xlim3d([0, x.max()])
    ax.set_ylim3d([0, y.max()])
    ax.set_zlim3d([0, z.max()])

    # Adding Figure Labels
    ax.set_title(f'Object Tracking 3D Mapping \nTime =  {np.round((time.time() - start_time), decimals=2)} seconds')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
# Plotting the Animation
fig = plt.figure()
ax = plt.axes(projection='3d')
line_ani = animation.FuncAnimation(fig, animate_func, interval=50, frames=numDataPoints, blit=False)
plt.show()

fn = './RealTime/output_images/sequential_sc3d'
#line_ani.save(fn+'.mp4',writer='ffmpeg',fps=1000/50)
line_ani.save(fn+'.gif',writer='imagemagick',fps=1000/50)