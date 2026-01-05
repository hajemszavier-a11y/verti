import bpy
import math

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import headband support (the fabric band part)
bpy.ops.wm.stl_import(filepath="VertiBand Head Support Final.stl")
headband = bpy.context.selected_objects[0]
headband.name = "Headband"

# Import electronics box (goes on the back)
bpy.ops.wm.stl_import(filepath="VertiBand Final.stl")
box = bpy.context.selected_objects[0]
box.name = "ElectronicsBox"

# Center everything
for obj in [headband, box]:
    obj.select_set(True)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
bpy.context.view_layer.objects.active = headband
bpy.ops.object.location_clear()

# BLACK FABRIC MATERIAL for headband (like Nike/athletic headband)
fabric_mat = bpy.data.materials.new(name="Black_Fabric_Headband")
fabric_mat.use_nodes = True
nodes = fabric_mat.node_tree.nodes
links = fabric_mat.node_tree.links
nodes.clear()

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)  # Deep black
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.9  # Fabric texture
bsdf.inputs['Specular IOR Level'].default_value = 0.2

output = nodes.new(type='ShaderNodeOutputMaterial')
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Assign to headband
if headband.data.materials:
    headband.data.materials[0] = fabric_mat
else:
    headband.data.materials.append(fabric_mat)

# DARK TECH MATERIAL for electronics box
tech_mat = bpy.data.materials.new(name="Electronics_Box")
tech_mat.use_nodes = True
nodes = tech_mat.node_tree.nodes
links = tech_mat.node_tree.links
nodes.clear()

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.inputs['Base Color'].default_value = (0.10, 0.10, 0.12, 1.0)  # Dark gray
bsdf.inputs['Metallic'].default_value = 0.4
bsdf.inputs['Roughness'].default_value = 0.3  # Smooth tech finish
bsdf.inputs['Specular IOR Level'].default_value = 0.6

output = nodes.new(type='ShaderNodeOutputMaterial')
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Assign to box
if box.data.materials:
    box.data.materials[0] = tech_mat
else:
    box.data.materials.append(tech_mat)

# Get dimensions for camera
bbox = headband.bound_box
min_point = [min([v[i] for v in bbox]) for i in range(3)]
max_point = [max([v[i] for v in bbox]) for i in range(3)]
size = [max_point[i] - min_point[i] for i in range(3)]
max_dim = max(size)

# Camera positioned to show headband + box on back (3/4 view)
cam_distance = max_dim * 1.8
bpy.ops.object.camera_add(location=(cam_distance * 0.9, -cam_distance * 1.1, cam_distance * 0.5))
camera = bpy.context.object
camera.rotation_euler = (math.radians(70), 0, math.radians(40))
bpy.context.scene.camera = camera

# Professional studio lighting
# Key light (main)
bpy.ops.object.light_add(type='AREA', location=(5, -5, 6))
key_light = bpy.context.object
key_light.data.energy = 400
key_light.data.size = 6

# Fill light (softer)
bpy.ops.object.light_add(type='AREA', location=(-4, -3, 4))
fill_light = bpy.context.object
fill_light.data.energy = 200
fill_light.data.size = 5

# Rim light (for separation)
bpy.ops.object.light_add(type='AREA', location=(0, 3, 5))
rim_light = bpy.context.object
rim_light.data.energy = 250
rim_light.data.size = 4

# Top light
bpy.ops.object.light_add(type='AREA', location=(0, 0, 8))
top_light = bpy.context.object
top_light.data.energy = 150
top_light.data.size = 7

# Clean white studio background
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
scene.cycles.samples = 192
scene.cycles.use_denoising = False
scene.render.resolution_x = 2000
scene.render.resolution_y = 2000
scene.render.film_transparent = False
scene.render.filepath = "/home/user/verti/vertiband-final.png"

bpy.ops.render.render(write_still=True)
print("Final VertiBand render complete!")
