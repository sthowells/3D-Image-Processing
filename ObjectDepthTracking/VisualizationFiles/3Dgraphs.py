import numpy as np
from numpy import loadtxt
import matplotlib.pyplot as plt

X = loadtxt('RealTime/spatial_loc/XX.txt')
Y = loadtxt('RealTime/spatial_loc//YY.txt')
Z = loadtxt('RealTime/spatial_loc/ZZ.txt')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X,Y,Z, c=Z.ravel())
ax.set_zlim(0, 100)
plt.show()