"""
import asyncio
from websockets import connect
import json
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

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

def animate(i, message):
    global xdata, ydata, zdata
    for line, pt in zip(lines, pts):
        message = json.loads(message)
        x = float(message["x"])
        y = float(message["y"])
        z = float(message["z"])
        # update trajectory list
        xdata.append(x)
        ydata.append(y)
        zdata.append(z)

        line.set_data(xdata, ydata)
        line.set_3d_properties(zdata)

        pt.set_data(xdata[-1:], ydata[-1:])
        pt.set_3d_properties(zdata[-1:])

    fig.canvas.draw()
    return lines + pts
# import cv2
# import base64

async def hello(uri):
    async with connect(uri) as websocket:
        for i in range(10):
            await websocket.send("Hello world")
            msg = await websocket.recv()
            print(msg)
            anim = animation.FuncAnimation(fig, animate, init_func=init, frames=10, interval=30, fargs=(msg), blit=True)
            plt.pause(0.1)

asyncio.run(hello("ws://localhost:8080"))
"""


"""
import asyncio
import websockets
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import time



loop = asyncio.get_event_loop()
# 接続
uri = "ws://localhost:8080"
websocket = loop.run_until_complete(websockets.connect(uri))



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

def animate(i, x, y, z):
    # print("animate")
    
    for line, pt in zip(lines, pts):
        print(x, y, z)
        # update trajectory list
        xdata.append(x)
        ydata.append(y)
        zdata.append(z)

        print(xdata)

        line.set_data(xdata, ydata)
        line.set_3d_properties(zdata)

        pt.set_data(xdata[-1:], ydata[-1:])
        pt.set_3d_properties(zdata[-1:])

    fig.canvas.draw()
    time.sleep(0.1)
    
    return lines + pts

"""



"""
fig = plt.figure()


def animate_test(i, x, y):
    plt.scatter(x, y)
    plt.pause(0.1)
"""

"""
# 送信
dictionary = {'message': 'Message from Client', 'number': 256, 'bool': True, "x": 0, "y": 0, "z": 0}
packet = json.dumps(dictionary).encode()
loop.run_until_complete(websocket.send(packet))

while True:
    # 受信
    received_packet = loop.run_until_complete(websocket.recv())
    result = json.loads(received_packet.decode())
    x = float(result["x"])
    y = float(result["y"])
    z = float(result["z"])

    # anim = animation.FuncAnimation(fig, animate_test, interval=100, fargs=(x, y), blit=True)
    anim = animation.FuncAnimation(fig, animate, interval=100, fargs=(x, y, z), blit=True)

    plt.pause(0.5)

    packet = json.dumps(result).encode()
    loop.run_until_complete(websocket.send(packet))

    
# 終了
loop.run_until_complete(websocket.close())
loop.close()
print("Finish.")
"""

import cv2
import requests
import asyncio
import websockets


loop = asyncio.get_event_loop()
uri = "ws://localhost:8080"
websocket = loop.run_until_complete(websockets.connect())

cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(cv2.CAP_PROP_FPS, 10)

frame_count = 0
frame_freq = 20


