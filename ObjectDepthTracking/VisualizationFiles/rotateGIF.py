import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from numpy import loadtxt

# Space Coordinate
X = loadtxt('RealTime/spatial_loc/XX.txt')
Y = loadtxt('RealTime/spatial_loc/YY.txt')
Z = loadtxt('RealTime/spatial_loc/ZZ.txt')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x-axes')
ax.set_ylabel('y-axes')
ax.set_zlabel('depth')
#ax.grid(False)
#ax.set_axis_off()

def init():
    ax.scatter(X,Y,Z, c=Z.ravel())
    ax.set_zlim(0, 100)
    return fig,

def animate(i):
    ax.view_init(elev=10., azim=2*i)
    return fig,

# Animate & Save files: mp4/gif
ani = animation.FuncAnimation(fig, animate, init_func=init,frames=360, interval=50, blit=True)    
fn = 'RealTime/output_images/rotate_azimuth_angle_3d_surf'
ani.save(fn+'.mp4',writer='ffmpeg',fps=1000/50)
ani.save(fn+'.gif',writer='imagemagick',fps=1000/50)