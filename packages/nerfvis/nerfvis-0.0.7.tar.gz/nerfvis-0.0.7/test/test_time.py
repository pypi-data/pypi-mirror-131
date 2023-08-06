import nerfvis

import numpy as np
scene = nerfvis.Scene("hello world")
scene.add_axes()
points1 = np.random.rand(50**3, 3)
points2 = np.random.rand(50**3, 3)
scene.add_points('Points_f1', points1, point_size=2, time=1)
scene.add_points('Points_f2', points2, point_size=2, time=2)
#  scene.add_mesh_from_file('/home/sxyu/data/example-models/teapot-low.obj')
scene.display(port=8080)
