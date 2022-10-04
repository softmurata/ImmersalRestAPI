import open3d as o3d
import random

# can only one object?

if __name__ == "__main__":
    o3d.visualization.webrtc_server.enable_webrtc()

    green_red = o3d.geometry.TriangleMesh.create_box(4, 2, 4)
    green_red.compute_vertex_normals()
    green_red.paint_uniform_color((0.0, 2.0, 0.0))
    # o3d.visualization.draw_geometries_with_animation_callback([cube_red],rotate_view)
    o3d.visualization.draw(green_red)
        

