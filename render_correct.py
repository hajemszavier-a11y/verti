import bpy
import math

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import the ELECTRONICS BOX (VertiBand Final = the main device)
bpy.ops.wm.stl_import(filepath="VertiBand Final.stl")
device = bpy.context.selected_objects[0]
device.name = "Device"

# Center it
device.location = (0, 0, 0)

# DARK PROFESSIONAL TECH MATERIAL for the electronics box
# (Like AirPods case, Apple products - premium dark plastic/metal)
tech_mat = bpy.data.materials.new(name="Tech_Device")
tech_mat.use_nodes = True
nodes = tech_mat.node_tree.nodes
links = tech_mat.node_tree.links
nodes.clear()

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
bsdf.inputs['Base Color'].default_value = (0.08, 0.08, 0.10, 1.0)  # Dark gray/black
bsdf.inputs['Metallic'].default_value = 0.3  # Slight metallic
bsdf.inputs['Roughness'].default_value = 0.35  # Smooth premium finish
bsdf.inputs['Specular IOR Level'].default_value = 0.5

output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (200, 0)
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Assign material to device
if device.data.materials:
    device.data.materials[0] = tech_mat
else:
    device.data.materials.append(tech_mat)

# Get object size for camera positioning
bbox = device.bound_box
min_point = [min([v[i] for v in bbox]) for i in range(3)]
max_point = [max([v[i] for v in bbox]) for i in range(3)]
size = [max_point[i] - min_point[i] for i in range(3)]
max_dim = max(size)

# Camera (product shot angle)
cam_distance = max_dim * 2.2
bpy.ops.object.camera_add(location=(cam_distance * 0.8, -cam_distance, cam_distance * 0.6))
camera = bpy.context.object
camera.rotation_euler = (math.radians(65), 0, math.radians(35))
bpy.context.scene.camera = camera

# Studio lighting (professional product photography)
# Key light
bpy.ops.object.light_add(type='AREA', location=(4, -4, 5))
key_light = bpy.context.object
key_light.data.energy = 350
key_light.data.size = 5

# Fill light
bpy.ops.object.light_add(type='AREA', location=(-3, -2, 3))
fill_light = bpy.context.object
fill_light.data.energy = 150
fill_light.data.size = 4

# Rim light (for edge definition)
bpy.ops.object.light_add(type='AREA', location=(0, 2, 4))
rim_light = bpy.context.object
rim_light.data.energy = 200
rim_light.data.size = 3

# Clean white background
world = bpy.context.scene.world
world.use_nodes = True
world_nodes = world.node_tree.nodes
world_nodes.clear()

bg = world_nodes.new(type='ShaderNodeBackground')
bg.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
bg.inputs['Strength'].default_value = 1.0

world_output = world_nodes.new(type='ShaderNodeOutputWorld')
world.node_tree.links.new(bg.outputs['Background'], world_output.inputs['Surface'])

# Render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.cycles.use_denoising = False
scene.render.resolution_x = 1800
scene.render.resolution_y = 1800
scene.render.film_transparent = False
scene.render.filepath = "/home/user/verti/vertiband-product.png"

bpy.ops.render.render(write_still=True)
print("Product render complete!")
