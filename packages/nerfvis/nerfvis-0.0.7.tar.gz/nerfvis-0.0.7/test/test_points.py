import nerfvis

import numpy as np
scene = nerfvis.Scene("hello world")
scene.add_axes()
points = np.random.rand(50**3, 3)
scene.add_points('Points', points, point_size=10)
#  scene.add_mesh_from_file('/home/sxyu/data/example-models/teapot-low.obj')
scene.display(port=8080)
