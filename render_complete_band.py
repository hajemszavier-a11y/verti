import bpy
import math

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create circular headband (torus for the fabric band)
bpy.ops.mesh.primitive_torus_add(
    major_radius=0.11,  # Head size
    minor_radius=0.015,  # Band thickness
    location=(0, 0, 0)
)
headband = bpy.context.object
headband.name = "FabricBand"
headband.rotation_euler = (math.radians(90), 0, 0)  # Stand it up

# BLACK FABRIC material for headband
fabric_mat = bpy.data.materials.new(name="Black_Headband_Fabric")
fabric_mat.use_nodes = True
nodes = fabric_mat.node_tree.nodes
links = fabric_mat.node_tree.links
nodes.clear()

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.inputs['Base Color'].default_value = (0.015, 0.015, 0.015, 1.0)  # Deep black
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.95  # Very matte fabric
bsdf.inputs['Specular IOR Level'].default_value = 0.15

output = nodes.new(type='ShaderNodeOutputMaterial')
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

headband.data.materials.append(fabric_mat)

# Import electronics box (curved to fit occipital area)
bpy.ops.wm.stl_import(filepath="VertiBand Final.stl")
box = bpy.context.selected_objects[0]
box.name = "ElectronicsBox"

# Position box at back of headband (integrated inside)
box.location = (0, 0.09, 0)  # At the back
box.scale = (0.8, 0.8, 0.8)  # Scale to fit inside band

# Dark tech material for box
tech_mat = bpy.data.materials.new(name="Electronics")
tech_mat.use_nodes = True
nodes = tech_mat.node_tree.nodes
links = tech_mat.node_tree.links
nodes.clear()

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.inputs['Base Color'].default_value = (0.09, 0.09, 0.11, 1.0)
bsdf.inputs['Metallic'].default_value = 0.5
bsdf.inputs['Roughness'].default_value = 0.25
bsdf.inputs['Specular IOR Level'].default_value = 0.6

output = nodes.new(type='ShaderNodeOutputMaterial')
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

if box.data.materials:
    box.data.materials[0] = tech_mat
else:
    box.data.materials.append(tech_mat)

# Camera angle to show full headband with box at back
bpy.ops.object.camera_add(location=(0.35, -0.25, 0.15))
camera = bpy.context.object
camera.rotation_euler = (math.radians(75), 0, math.radians(55))
bpy.context.scene.camera = camera

# Professional lighting
bpy.ops.object.light_add(type='AREA', location=(0.4, -0.3, 0.4))
key_light = bpy.context.object
key_light.data.energy = 80
key_light.data.size = 0.5

bpy.ops.object.light_add(type='AREA', location=(-0.3, -0.2, 0.3))
fill_light = bpy.context.object
fill_light.data.energy = 40
fill_light.data.size = 0.4

bpy.ops.object.light_add(type='AREA', location=(0, 0.3, 0.3))
rim_light = bpy.context.object
rim_light.data.energy = 50
rim_light.data.size = 0.3

# White studio background
world = bpy.context.scene.world
world.use_nodes = True
world_nodes = world.node_tree.nodes
world_nodes.clear()

bg = world_nodes.new(type='ShaderNodeBackground')
bg.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
bg.inputs['Strength'].default_value = 1.0

world_output = world_nodes.new(type='ShaderNodeOutputWorld')
world.node_tree.links.new(bg.outputs['Background'], world_output.inputs['Surface'])

# Render
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 156
scene.cycles.use_denoising = False
scene.render.resolution_x = 1800
scene.render.resolution_y = 1800
scene.render.film_transparent = False
scene.render.filepath = "/home/user/verti/vertiband-complete.png"

bpy.ops.render.render(write_still=True)
print("Complete VertiBand headband rendered!")
