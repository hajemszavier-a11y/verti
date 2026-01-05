import bpy
import math

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import ONE component to test
bpy.ops.wm.stl_import(filepath="VertiBand Final.stl")
obj = bpy.context.selected_objects[0]

# Get bounds
bbox = obj.bound_box
min_point = [min([v[i] for v in bbox]) for i in range(3)]
max_point = [max([v[i] for v in bbox]) for i in range(3)]
size = [max_point[i] - min_point[i] for i in range(3)]
max_dim = max(size)

print(f"Object bounds: min={min_point}, max={max_point}")
print(f"Object size: {size}")
print(f"Max dimension: {max_dim}")

# Center object at origin
obj.location = (0, 0, 0)

# Simple black material
mat = bpy.data.materials.new(name="Black")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
bsdf.inputs['Roughness'].default_value = 0.7

if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)

# Camera positioned to see the object
cam_distance = max_dim * 2.5
bpy.ops.object.camera_add(location=(cam_distance, -cam_distance, cam_distance * 0.7))
camera = bpy.context.object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))
bpy.context.scene.camera = camera

# Simple lighting
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
sun = bpy.context.object
sun.data.energy = 3

# White world
world = bpy.context.scene.world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (1, 1, 1, 1)
bg.inputs['Strength'].default_value = 1

# Render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.use_denoising = False
scene.render.resolution_x = 1200
scene.render.resolution_y = 1200
scene.render.film_transparent = False
scene.render.filepath = "/home/user/verti/test-render.png"

bpy.ops.render.render(write_still=True)
print("Test render complete!")
