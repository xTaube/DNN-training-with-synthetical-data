import bpy
import sys
import os
import numpy as np

src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(src_dir))
sys.path.append(os.path.join(src_dir, "venv", "lib", "python3.7", "site-packages"))
sys.path.append("/home/majkel/.local/lib/python3.10/site-packages")

from pyquaternion import Quaternion
import src.render.blender as bld
import src.render as render


render_filepath = os.path.join(src_dir)
scene = bld.Scene(bpy.data.scenes[0], render_engine="CYCLES", file_format="OPEN_EXR")
cube = bld.Cube(reference=bpy.data.objects['Cube'])
cube.delete()

background = render.draw_background(os.path.join(src_dir, "resources", "backgrounds"))
scene.set_background(background)

for _ in range(5):
    category = render.draw_category(os.path.join(src_dir, "resources", "categories"))
    model_path = render.draw_model(os.path.join(src_dir, 'resources', "categories", category))
    scale = np.random.uniform(10, 16)
    location = np.random.uniform(-5, 5, 3)
    rotation = Quaternion.random()
    model = bld.ImportedObject(path=model_path, location=tuple(location), scale=scale, rotation=rotation)
    texture_path = render.get_model_texture_path(model_path)
    model.add_texture(texture_path)
    model.metadata["category"] = category
    model.metadata["scale"] = scale
    scene.add_object(model)

camera = bld.Camera(reference=bpy.data.objects['Camera'], location=(40, -8, 3))
scene.set_camera(camera)

camera.look_at((0, 0, 0))

frame = scene.render_image(["RGB", "segmentation"])
render.save_rgb_array_as_png(frame["RGB"], os.path.join(src_dir, "rgb.png"))
render.save_segmentation_array_as_png(frame["segmentation"], os.path.join(src_dir, "seg.png"))
