"""
from matplotlib import pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
# import matplotlib as mpl
# mpl.use('tkagg')


fig = plt.figure()
ax = p3.Axes3D(fig)


x = 1.0
y = 2.0
z = 2.0

points, = ax.plot([x], [y], [z], '*')
txt = fig.suptitle('')

previous_points = [x, y, z]

dummy_x = np.arange(0, 1, 10)
dummy_y = np.arange(0, 1, 10)
dummy_z = np.arange(0, 1, 10)

def update(num, x, y, z, points, previous_points):
    txt.set_text('num={:d}'.format(num)) # for debug purposes

    # calculate the new sets of coordinates here. The resulting arrays should have the same shape
    # as the original x,y,z
    print(previous_points)
    new_x = previous_points[0]+0.1
    new_y = previous_points[1]+0.1
    new_z = previous_points[2]+0.1
    
    previous_points = [new_x, new_y, new_z]

    # update properties
    points.set_data(new_x, new_y)
    points.set_3d_properties(new_z, 'z')

    # return modified artists
    return points,txt,previous_points


def update_points(num, x, y, z, points):
    txt.set_text('num={:d}'.format(num)) # for debug purposes

    # calculate the new sets of coordinates here. The resulting arrays should have the same shape
    # as the original x,y,z
    new_x = x+np.random.normal(1,0.1, size=(len(x),))
    new_y = y+np.random.normal(1,0.1, size=(len(y),))
    new_z = z+np.random.normal(1,0.1, size=(len(z),))

    # update properties
    points.set_data(new_x,new_y)
    points.set_3d_properties(new_z, 'z')

    # return modified artists
    return points,txt

# ani=animation.FuncAnimation(fig, update_points, frames=10, fargs=(x, y, z, points))
ani = animation.FuncAnimation(fig, update, frames=10, fargs=(dummy_x, dummy_y, dummy_z, points, previous_points))

plt.show()
"""
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
 
# References
# https://gist.github.com/neale/e32b1f16a43bfdc0608f45a504df5a84
# https://towardsdatascience.com/animations-with-matplotlib-d96375c5442c
# https://riptutorial.com/matplotlib/example/23558/basic-animation-with-funcanimation
 
# ANIMATION FUNCTION
def func(num, dataSet, line):
    # NOTE: there is no .set_data() for 3 dim data...
    line.set_data(dataSet[0:2, :num])    
    line.set_3d_properties(dataSet[2, :num])    
    return line
 
 
# THE DATA POINTS
t = np.arange(0,20,0.2) # This would be the z-axis ('t' means time here)
x = np.cos(t)-1
y = 1/2*(np.cos(2*t)-1)
dataSet = np.array([x, y, t])
numDataPoints = len(t)
 
# GET SOME MATPLOTLIB OBJECTS
fig = plt.figure()
ax = Axes3D(fig)
 
# NOTE: Can't pass empty arrays into 3d version of plot()
# line = plt.plot(dataSet[0], dataSet[1], dataSet[2], lw=2, c='g')[0] # For line plot
points, = ax.plot(dataSet[0], dataSet[1], dataSet[2], '*')
 
# AXES PROPERTIES]
# ax.set_xlim3d([limit0, limit1])
ax.set_xlabel('X(t)')
ax.set_ylabel('Y(t)')
ax.set_zlabel('time')
ax.set_title('Trajectory of electron for E vector along [120]')
 
# Creating the Animation object
line_ani = animation.FuncAnimation(fig, func, frames=numDataPoints, fargs=(dataSet,points), interval=50, blit=False)
#line_ani.save(r'AnimationNew.mp4')
 
 
plt.show()
"""

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

# choose random starting points
np.random.seed(1)

fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection="3d")


N_trajectories = 1

colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))

lines = sum([ax.plot([], [], [], '-', c=c) for c in colors], [])
pts = sum([ax.plot([], [], [], 'o', c=c) for c in colors], [])

ax.set_xlim((-25, 25))
ax.set_ylim((-35, 35))
ax.set_zlim((5, 55))

ax.view_init(30, 0)

x0 = 1.0
y0 = 1.0
z0 = 1.0

def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])

    return lines + pts


xdata = []
ydata = []
zdata = []

def animate(i):
    for line, pt in zip(lines, pts):
        x = x0 + 2 * np.cos(i * np.pi / 2)
        y = y0 + 3 * np.sin(i * np.pi / 2)
        z = z0 + i * 0.3

        # update trajectory list
        xdata.append(x)
        ydata.append(y)
        zdata.append(z)

        line.set_data(xdata, ydata)
        line.set_3d_properties(zdata)

        pt.set_data(xdata[-1:], ydata[-1:])
        pt.set_3d_properties(zdata[-1:])

    fig.canvas.draw()
    return lines + pts, xdata, ydata, zdata


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=30)

plt.show()


"""
import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

N_trajectories = 20


def lorentz_deriv(points, t0, sigma=10., beta=8./3, rho=28.0):
    
    x, y, z = points
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

# Choose random starting points, uniformly distributed from -15 to 15
np.random.seed(1)
x0 = -15 + 30 * np.random.random((N_trajectories, 3))

# Solve for the trajectories
t = np.linspace(0, 4, 1000)
x_t = np.asarray([integrate.odeint(lorentz_deriv, x0i, t)
                  for x0i in x0])

# Set up figure & 3D axis for animation
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('off')

# choose a different color for each trajectory
colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))

# set up lines and points
lines = sum([ax.plot([], [], [], '-', c=c)
             for c in colors], [])
pts = sum([ax.plot([], [], [], 'o', c=c)
           for c in colors], [])

# prepare the axes limits
ax.set_xlim((-25, 25))
ax.set_ylim((-35, 35))
ax.set_zlim((5, 55))

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 0)

# initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines + pts

# animation function.  This will be called sequentially with the frame number
def animate(i):
    # we'll step two time-steps per frame.  This leads to nice results.
    i = (2 * i) % x_t.shape[1]

    for line, pt, xi in zip(lines, pts, x_t):
        x, y, z = xi[:i].T
        print(x, y, z, x[:i])
        line.set_data(x, y)
        line.set_3d_properties(z)

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])

    ax.view_init(30, 0.3 * i)
    fig.canvas.draw()
    return lines + pts

# instantiate the animator.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=500, interval=30, blit=True)

# Save as mp4. This requires mplayer or ffmpeg to be installed
#anim.save('lorentz_attractor.mp4', fps=15, extra_args=['-vcodec', 'libx264'])

plt.show()
"""

