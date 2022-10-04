
import argparse
import open3d as o3d
import numpy as np
import open3d.visualization.gui as gui


# data sample
data1106 = {
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

data1107 = {
	"error":	"none",
	"success":	True,
	"map":	41769,
	"px":	-0.39470410346984863,
	"py":	-0.1166694164276123,
	"pz":	-1.0279941558837891,
	"r00":	-0.049044195562601089,
	"r01":	0.036461509764194489,
	"r02":	-0.99813085794448853,
	"r10":	0.033391758799552917,
	"r11":	-0.99871498346328735,
	"r12":	-0.038123585283756256,
	"r20":	-0.99823826551437378,
	"r21":	-0.035199087113142014,
	"r22":	0.047763656824827194,
	"time":	0.674150969
}

data1108 = {
	"error":	"none",
	"success":	True,
	"map":	41769,
	"px":	-0.33669471740722656,
	"py":	-0.1006210595369339,
	"pz":	-0.16397719085216522,
	"r00":	-0.909222424030304,
	"r01":	-0.055619925260543823,
	"r02":	-0.4125785231590271,
	"r10":	0.064895667135715485,
	"r11":	-0.99785590171813965,
	"r12":	-0.0084927398711442947,
	"r20":	-0.41122156381607056,
	"r21":	-0.034496348351240158,
	"r22":	0.91088241338729858,
	"time":	0.692428011
}

data1109 = {
	"error":	"none",
	"success":	True,
	"map":	41769,
	"px":	-0.1588224470615387,
	"py":	-0.18498235940933228,
	"pz":	-0.15928563475608826,
	"r00":	-0.924305260181427,
	"r01":	-0.046692486852407455,
	"r02":	-0.37878704071044922,
	"r10":	0.048535831272602081,
	"r11":	-0.99881047010421753,
	"r12":	0.004686061292886734,
	"r20":	-0.37855526804924011,
	"r21":	-0.01405339315533638,
	"r22":	0.92547202110290527,
	"time":	1.127389618
}

flip_transform = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]

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

    colors = [[1, 0, 0] for i in range(len(lines))]
    lineset = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(points),
        lines=o3d.utility.Vector2iVector(lines)
    )
    lineset.colors = o3d.utility.Vector3dVector(colors)

    trans = create_transform_matrix_from_data(data)

    lineset.transform(trans)
    lineset.transform(flip_transform)

    camera_points = np.asarray(lineset.points)[-1] + 0.1

    return lineset, camera_points


def create_transform_matrix_from_data(data):

    trans = [[float(data["r00"]), float(data["r01"]), float(data["r02"]), float(data["px"])],
        [float(data["r10"]), float(data["r11"]), float(data["r12"]), float(data["py"])],
        [float(data["r20"]), float(data["r21"]), float(data["r22"]), float(data["pz"])],
        [0, 0, 0, 1]
    ]

    return trans


parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, default="data1106")
args = parser.parse_args()


o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)
# load point cloud file
source_raw = o3d.io.read_point_cloud("yamabuki0117.ply")
source = source_raw.voxel_down_sample(voxel_size=0.02)
# source.transform(flip_transform)

lineset1106, camera1106 = create_camera_frame(data1106)
lineset1107, camera1107 = create_camera_frame(data1107)
lineset1108, camera1108 = create_camera_frame(data1108)
lineset1109, camera1109 = create_camera_frame(data1109)


app = gui.Application.instance
app.initialize()

vis = o3d.visualization.O3DVisualizer("Open3D - 3D Text", 1024, 768)
vis.show_settings = True
vis.add_geometry("source", source)
vis.add_geometry("lineset1106", lineset1106)
# vis.add_geometry("lineset1107", lineset1107)
# vis.add_geometry("lineset1108", lineset1108)
# vis.add_geometry("lineset1109", lineset1109)

vis.add_3d_label(camera1106, "data1106")
# vis.add_3d_label(camera1107, "data1107")
# vis.add_3d_label(camera1108, "data1108")
# vis.add_3d_label(camera1109, "data1109")

vis.reset_camera_to_default()

app.add_window(vis)
app.run()




"""
vis = o3d.visualization.Visualizer()
vis.create_window()
colors = [[1, 0, 0] for i in range(len(lines))]
lineset = o3d.geometry.LineSet(
    points=o3d.utility.Vector3dVector(points),
    lines=o3d.utility.Vector2iVector(lines)
)
lineset.colors = o3d.utility.Vector3dVector(colors)

if args.data_path == "data1106":
    data = data1106
elif args.data_path == "data1107":
    data = data1107
elif args.data_path == "data1108":
    data = data1108
else:
    data = data1109

trans = create_transform_matrix_from_data(data)

lineset.transform(trans)
lineset.transform(flip_transform)

vis.add_geometry(lineset)
vis.add_geometry(source)
ctr = vis.get_view_control()
ctr.rotate(-180.0, 0)
vis.run()
vis.destroy_window()
"""


"""
# add text label
import numpy as np
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering


def make_point_cloud(npts, center, radius):
    pts = np.random.uniform(-radius, radius, size=[npts, 3]) + center
    cloud = o3d.geometry.PointCloud()
    cloud.points = o3d.utility.Vector3dVector(pts)
    colors = np.random.uniform(0.0, 1.0, size=[npts, 3])
    cloud.colors = o3d.utility.Vector3dVector(colors)
    return cloud


app = gui.Application.instance
app.initialize()

points = make_point_cloud(100, (0, 0, 0), 1.0)

vis = o3d.visualization.O3DVisualizer("Open3D - 3D Text", 1024, 768)
vis.show_settings = True
vis.add_geometry("Points", points)
for idx in range(0, len(points.points)):
    vis.add_3d_label(points.points[idx], "{}".format(idx))
vis.reset_camera_to_default()

app.add_window(vis)
app.run()
"""





"""
# animation

import open3d as o3d
import numpy as np

o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)
source_raw = o3d.io.read_point_cloud("yamabuki.ply")

source = source_raw.voxel_down_sample(voxel_size=0.02)
trans = [[0.862, 0.011, -0.507, 0.0], [-0.139, 0.967, -0.215, 0.7],
             [0.487, 0.255, 0.835, -1.4], [0.0, 0.0, 0.0, 1.0]]
source.transform(trans)

flip_transform = [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]
source.transform(flip_transform)

source_center = source.get_center().tolist()

## ref: http://whitewell.sakura.ne.jp/Open3D/Visualization.html#Draw-line-set
size = 0.5
points = [
    [source_center[0], source_center[1], source_center[2]],
    [source_center[0] + size, source_center[1], source_center[2]],
    [source_center[0], source_center[1] + size, source_center[2]],
    [source_center[0] + size, source_center[1] + size, source_center[2]],
    [source_center[0] + 0.5 * size, source_center[1] + 0.5 * size, source_center[2] + 0.5 * size]
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

vis = o3d.visualization.Visualizer()
vis.create_window()

colors = [[1, 0, 0] for i in range(len(lines))]
lineset = o3d.geometry.LineSet(
    points=o3d.utility.Vector3dVector(points),
    lines=o3d.utility.Vector2iVector(lines)
)
lineset.colors = o3d.utility.Vector3dVector(colors)
vis.add_geometry(lineset)
vis.add_geometry(source)

# only visualize
# ctr = vis.get_view_control()
# ctr.change_field_of_view(step=90)
# vis.run()
# vis.destroy_window()


scale = 0.01

for i in range(100):

    new_points = [
    [source_center[0] + i * scale, source_center[1] + i * scale, source_center[2]],
    [source_center[0] + size + i * scale, source_center[1] + i * scale, source_center[2]],
    [source_center[0] + i * scale, source_center[1] + size + i * scale, source_center[2]],
    [source_center[0] + size + i * scale, source_center[1] + size + i * scale, source_center[2]],
    [source_center[0] + 0.5 * size + i * scale, source_center[1] + 0.5 * size + i * scale, source_center[2] + 0.5 * size]
    ]

    pts = o3d.utility.Vector3dVector(new_points)
    lineset.points = pts
    vis.update_geometry(lineset)
    vis.poll_events()
    vis.update_renderer()
vis.destroy_window()

"""


