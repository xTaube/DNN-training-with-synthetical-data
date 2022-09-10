import bpy
import sys
import os
import numpy as np

src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(src_dir))
sys.path.append(os.path.join(src_dir, "venv", "Lib", "site-packages"))
sys.path.append(os.path.join(src_dir, "venv", "Lib", "site-packages", "OpenEXR.cp37-win_amd64.pyd"))
import src.render.blender as bld


render_filepath = os.path.join(src_dir)
scene = bld.Scene(bpy.data.scenes[0], render_engine="CYCLES", render_filepath=render_filepath, file_format="OPEN_EXR")
cube = bld.Cube(reference=bpy.data.objects['Cube'])
scene.add_object(cube)

for _ in range(20):
    c = bld.Cube(location=(np.random.uniform(-5, 5), np.random.uniform(-5, 5), np.random.uniform(-5, 5)))
    scene.add_object(c)

camera = bld.Camera(reference=bpy.data.objects['Camera'], location=(-15.23, -8, 3))
scene.set_camera(camera)

camera.look_at(cube.location)

frame = scene.render_image()
print(frame)
