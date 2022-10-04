# animation

import open3d as o3d
import numpy as np
import cv2
import json
import requests
import base64
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



# settings for immersal sdk api
url = "https://api.immersal.com/1.15.0"
token = "52df255a3971bd4062048b1fed79494f7af9281270b1fffce4bfe30d3520d823"
email = "tatsuromurata317@gmail.com"
password = "rtfd2018"
mapId = 42209

cap = cv2.VideoCapture("IMG_1118.MOV")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(cv2.CAP_PROP_FPS, 10)
print(f"size: ({width}, {height})")


def ServerLocalize(url, token, b64img, mapId=42209):
    complete_url = url + '/localizeb64'

    data = {
        "token": token,
        "fx": 1455.738159, # image focal length in pixels on x axis
        "fy": 1455.738159, # image focal length in pixels on y axis
        "ox": 962.615967, # image principal point on x axis
        "oy": 694.292175, # image principal point on y axis
        "b64": str(b64img, "utf-8"), # base64 encoded .png image
        "mapIds": [{"id": mapId}] # a list of map ids to localize against
    }

    json_data = json.dumps(data)

    r = requests.post(complete_url, data=json_data)

    return r.json()

def create_camera_frame(data):
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

    colors = [[0, 1, 0] for i in range(len(lines))]
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



o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)
source_raw = o3d.io.read_point_cloud("yamabuki0121.ply")

source = source_raw.voxel_down_sample(voxel_size=0.02)
"""
init_trans = [[0.862, 0.011, -0.507, 0.0], [-0.139, 0.967, -0.215, 0.7],
             [0.487, 0.255, 0.835, -1.4], [0.0, 0.0, 0.0, 1.0]]
"""
init_trans = matrix([-90, 180, 0], [0, 0, 0])
source.transform(init_trans)
# source_center = source.get_center().tolist()

## ref: http://whitewell.sakura.ne.jp/Open3D/Visualization.html#Draw-line-set

vis = o3d.visualization.Visualizer()
vis.create_window()

# Initializxe camera frame
ret, frame = cap.read()
retval, buffer = cv2.imencode(".png", frame)
b64img = base64.b64encode(buffer)
init_data = ServerLocalize(url, token, b64img)

lineset, camera = create_camera_frame(init_data)
lineset.transform(init_trans)
vis.add_geometry(lineset)
vis.add_geometry(source)
# vis.run()
# exit()

# only visualize
# ctr = vis.get_view_control()
# ctr.change_field_of_view(step=90)
# vis.run()
# vis.destroy_window()

scale = 0.01

for i in range(250):
    """
    new_points = [
    [source_center[0] + i * scale, source_center[1] + i * scale, source_center[2]],
    [source_center[0] + size + i * scale, source_center[1] + i * scale, source_center[2]],
    [source_center[0] + i * scale, source_center[1] + size + i * scale, source_center[2]],
    [source_center[0] + size + i * scale, source_center[1] + size + i * scale, source_center[2]],
    [source_center[0] + 0.5 * size + i * scale, source_center[1] + 0.5 * size + i * scale, source_center[2] + 0.5 * size]
    ]

    pts = o3d.utility.Vector3dVector(new_points)
    lineset.points = pts
    """
    ret, frame = cap.read()

    retval, buffer = cv2.imencode(".png", frame)
    b64img = base64.b64encode(buffer)
    data = ServerLocalize(url, token, b64img)
    temp, camera = create_camera_frame(data)
    lineset.points = temp.points
    lineset.colors = temp.colors
    lineset.transform(init_trans)  # init transform
    cv2.imshow("window", frame)
    vis.update_geometry(lineset)
    vis.poll_events()
    vis.update_renderer()
vis.destroy_window()