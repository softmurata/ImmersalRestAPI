
import asyncio
import websockets
import json


import open3d as o3d
import numpy as np

from math import cos, sin, radians

def trig(angle):
    r = radians(angle)
    return cos(r), sin(r)

def matrix(rotation, translation):
    xC, xS = trig(rotation[0])
    yC, yS = trig(rotation[1])
    zC, zS = trig(rotation[2])
    dX = translation[0]
    dY = translation[1]
    dZ = translation[2]
    Translate_matrix = np.array([[1, 0, 0, dX],
                                [0, 1, 0, dY],
                                [0, 0, 1, dZ],
                                [0, 0, 0, 1]])
    Rotate_X_matrix = np.array([[1, 0, 0, 0],
                                [0, xC, -xS, 0],
                                [0, xS, xC, 0],
                                [0, 0, 0, 1]])
    Rotate_Y_matrix = np.array([[yC, 0, yS, 0],
                                [0, 1, 0, 0],
                                [-yS, 0, yC, 0],
                                [0, 0, 0, 1]])
    Rotate_Z_matrix = np.array([[zC, -zS, 0, 0],
                                [zS, zC, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])
    return np.dot(Rotate_Z_matrix,np.dot(Rotate_Y_matrix,np.dot(Rotate_X_matrix,Translate_matrix)))



def create_camera_frame(data):
    # ToDo: Problem: camera frame drawing....
    points = [
        [0.25, 0.25, 0.125],
        [-0.25, 0.25, 0.125],
        [0.25, -0.25, 0.125],
        [-0.25, -0.25, 0.125],
        [0, 0, 0]
    ]

    lines = [
        [0, 1],
        [0, 2],
        [1, 3],
        [2, 3],
        [0, 4],
        [1, 4],
        [2, 4],
        [3, 4]
    ]

    colors = [[1, 0, 0] for i in range(len(lines))]
    lineset = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(points),
        lines=o3d.utility.Vector2iVector(lines)
    )
    lineset.colors = o3d.utility.Vector3dVector(colors)

    trans = create_transform_matrix_from_data(data)

    lineset.transform(trans)
    # lineset.transform(flip_transform)

    camera_points = np.asarray(lineset.points)[-1] + 0.1

    return lineset, camera_points


def create_transform_matrix_from_data(data):

    trans = [[float(data["r00"]), float(data["r01"]), float(data["r02"]), float(data["px"])],
        [float(data["r10"]), float(data["r11"]), float(data["r12"]), float(data["py"])],
        [float(data["r20"]), float(data["r21"]), float(data["r22"]), float(data["pz"])],
        [0, 0, 0, 1]
    ]

    return trans


address = "localhost"
port = 8080


o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)
source_raw = o3d.io.read_point_cloud("yamabuki0121.ply")

source = source_raw.voxel_down_sample(voxel_size=0.02)
init_trans = matrix([-90, 180, 0], [0, 0, 0])
source.transform(init_trans)
# default
# trans = [[0.862, 0.011, -0.507, 0.0], [-0.139, 0.967, -0.215, 0.7],
#              [0.487, 0.255, 0.835, -1.4], [0.0, 0.0, 0.0, 1.0]]
# source.transform(trans)

vis = o3d.visualization.Visualizer()
vis.create_window()

"""
init_data = {
	"error":	"none",
	"success":	True,
	"map":	41769,
	"px":	0,
	"py":	0,
	"pz":	0,
	"r00":	0,
	"r01":	0,
	"r02":	0,
	"r10":	0,
	"r11":	0,
	"r12":	0,
	"r20":	0,
	"r21":	0,
	"r22":	0,
	"time":	-1
}
"""

init_data = {
	"error":	"none",
	"success":	True,
	"map":	41769,
	"px":	-0.46422445774078369,
	"py":	-0.1678304523229599,
	"pz":	-0.58463960886001587,
	"r00":	-0.10892344266176224,
	"r01":	0.050383813679218292,
	"r02":	-0.99277245998382568,
	"r10":	0.024300536140799522,
	"r11":	-0.99828124046325684,
	"r12":	-0.053329557180404663,
	"r20":	-0.99375307559967041,
	"r21":	-0.029933741316199303,
	"r22":	0.10751187056303024,
	"time":	0.659048038
}

lineset, camera = create_camera_frame(init_data)
lineset.transform(init_trans)
vis.add_geometry(lineset)
vis.add_geometry(source)


# 受信コールバック
async def server(websocket, path):
    while True:
        # 受信
        received_packet = await websocket.recv()
        dictionary = json.loads(received_packet.decode())
        # print("{}: {}".format(path, dictionary))
        # print(dictionary["success"])
        if dictionary["success"] != "false":
            temp, camera = create_camera_frame(dictionary)
            lineset.points = temp.points
            lineset.colors = temp.colors
            lineset.transform(init_trans)
            vis.update_geometry(lineset)
            vis.poll_events()
            vis.update_renderer()

            # 送信
            result = {"ok": "ok"}
            packet = json.dumps(result).encode()
            await websocket.send(packet)
        else:

            result = {"nook": "nook"}
            packet = json.dumps(result).encode()
            await websocket.send(packet)


    vis.destroy_window()
start_server = websockets.serve(server, address, port)
# サーバー立ち上げ
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
