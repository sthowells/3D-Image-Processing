import numpy as np
from numpy import loadtxt
import matplotlib.pyplot as plt

X = loadtxt('RealTime/spatial_loc/XX.txt')
Y = loadtxt('RealTime/spatial_loc//YY.txt')
Z = loadtxt('RealTime/spatial_loc/ZZ.txt')
stack = np.vstack(np.meshgrid(X,Y,Z)).reshape(3,-1).T
#print(stack)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(X,Y,Z, linewidth=0.2, antialiased=True)
ax.set_zlim(0, 100)

plt.show()