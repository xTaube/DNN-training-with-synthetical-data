import bpy
import math
import numpy as np


def rotate(point, angle_degrees, axis=(0, 1, 0)):
    theta_degrees = angle_degrees
    theta_radians = math.radians(theta_degrees)

    rotated_point = np.dot(rotation_matrix(axis, theta_radians), point)

    return rotated_point


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


bpy.ops.mesh.primitive_cube_add(size=3, location=(0, 0, 1.5))
cube = bpy.context.active_object
bpy.ops.mesh.primitive_plane_add(size=50)
plane = bpy.context.active_object

light_data = bpy.data.lights.new('light', type='SUN')

light = bpy.data.objects.new('light', light_data)
bpy.context.collection.objects.link(light)
light.location = (3, -4, 5)
light.data.energy = 200.0

# create camera
cam_data = bpy.data.cameras.new('camera')
cam = bpy.data.objects.new('camera', cam_data)
cam.location = (25, -3, 20)

constraint = cam.constraints.new(type='TRACK_TO')
constraint.target = cube

bpy.context.collection.objects.link(cam)

# create material
mat = bpy.data.materials.new(name='Material')
mat.use_nodes = True
mat_nodes = mat.node_tree.nodes
mat_links = mat.node_tree.links

cube.data.materials.append(mat)

# metallic
mat_nodes['Principled BSDF'].inputs['Metallic'].default_value = 1.0
mat_nodes['Principled BSDF'].inputs['Base Color'].default_value = (
0.005634391214698553, 0.01852927729487419, 0.8000000715255737, 1.0)
mat_nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.167
# 0.005634391214698553
# 0.01852927729487419
# 0.8000000715255737
# 1.0

# create material
mat = bpy.data.materials.new(name='Material')
mat.use_nodes = True
mat_nodes = mat.node_tree.nodes
mat_links = mat.node_tree.links

plane.data.materials.append(mat)

mat_nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.010, 0.065, 0.8, 1.0)

mat_nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.5

scene = bpy.context.scene
scene.camera = cam
scene.render.image_settings.file_format = 'PNG'

for angle in range(0, 360, 10):
    cam_location = cam.location
    cam.location = rotate(cam_location, 10, axis=(0, 0, 1))

    scene.render.filepath = f'C:\\Users\\mmeye\\PycharmProjects\\DNN-training-with-synthetical-data\\blender_{angle}.png'
    bpy.ops.render.render(write_still=1)