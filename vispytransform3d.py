"""
# Samples
import numpy as np
import matplotlib.pyplot as plt
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager


random_state = np.random.RandomState(0)

ee2robot = pt.transform_from_pq(
    np.hstack((np.array([0.4, -0.3, 0.5]),
               pr.random_quaternion(random_state))))
cam2robot = pt.transform_from_pq(
    np.hstack((np.array([0.0, 0.0, 0.8]), pr.q_id)))
object2cam = pt.transform_from(
    pr.active_matrix_from_intrinsic_euler_xyz(np.array([0.0, 0.0, -0.5])),
    np.array([0.5, 0.1, 0.1]))

tm = TransformManager()
tm.add_transform("end-effector", "robot", ee2robot)
tm.add_transform("camera", "robot", cam2robot)
tm.add_transform("object", "camera", object2cam)

ee2object = tm.get_transform("end-effector", "object")

ax = tm.plot_frames_in("robot", s=0.1)
ax.set_xlim((-0.25, 0.75))
ax.set_ylim((-0.5, 0.5))
ax.set_zlim((0.0, 1.0))
plt.show()
"""

"""
# visualize moving robot
import os
import numpy as np
from pytransform3d.urdf import UrdfTransformManager
import pytransform3d.visualizer as pv

def animation_callback(step, n_frames, tm, graph, joint_names):
    angle = 0.5 * np.cos(2.0 * np.pi * (step / n_frames))
    for joint_name in joint_names:
        tm.set_joint(joint_name, angle)
    graph.set_data()
    return graph

BASE_DIR = "pytransform3d/test/test_data/"
data_dir = BASE_DIR
search_path = "."
while (not os.path.exists(data_dir) and
       os.path.dirname(search_path) != "pytransform3d"):
    search_path = os.path.join(search_path, "..")
    data_dir = os.path.join(search_path, BASE_DIR)

tm = UrdfTransformManager()
filename = os.path.join(data_dir, "robot_with_visuals.urdf")
with open(filename, "r") as f:
    robot_urdf = f.read()
    tm.load_urdf(robot_urdf, mesh_path=data_dir)

joint_names = ["joint%d" % i for i in range(1, 7)]
for joint_name in joint_names:
    tm.set_joint(joint_name, 0.5)

fig = pv.figure()
graph = fig.plot_graph(
    tm, "robot_arm", s=0.1, show_frames=True, show_visuals=True)

fig.view_init()
fig.set_zoom(1.5)
n_frames = 100

if "__file__" in globals():
    fig.animate(animation_callback, n_frames, loop=True,
                fargs=(n_frames, tm, graph, joint_names))
    fig.show()
else:
    fig.save_image("__open3d_rendered_image.jpg")
"""
import numpy as np
import pytransform3d.visualizer as pv
from pytransform3d.rotations import matrix_from_angle, R_id
from pytransform3d.transformations import transform_from, concat


def update_trajectory(step, n_frames, trajectory):
    progress = 1 - float(step + 1) / float(n_frames)
    H = np.zeros((100, 4, 4))
    H0 = transform_from(R_id, np.zeros(3))
    H_mod = np.eye(4)
    for i, t in enumerate(np.linspace(0, progress, len(H))):
        H0[:3, 3] = np.array([t, 0, t])
        H_mod[:3, :3] = matrix_from_angle(2, 8 * np.pi * t)
        H[i] = concat(H0, H_mod)

    trajectory.set_data(H)
    return trajectory


n_frames = 200

fig = pv.figure()

H = np.empty((100, 4, 4))
H[:] = np.eye(4)
# set initial trajectory to extend view box
H[:, 0, 3] = np.linspace(-2, 2, len(H))
H[:, 1, 3] = np.linspace(-2, 2, len(H))
H[:, 2, 3] = np.linspace(0, 4, len(H))
trajectory = pv.Trajectory(H, s=0.2, c=[0, 0, 0])
trajectory.add_artist(fig)
fig.view_init()
fig.set_zoom(0.5)

if "__file__" in globals():
    fig.animate(
        update_trajectory, n_frames, fargs=(n_frames, trajectory), loop=True)
    fig.show()
else:
    fig.save_image("__open3d_rendered_image.jpg")


result = {
	"error":	"none",
	"success":	false,
	"map":	-1,
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
	"time":	0.898588088
}
