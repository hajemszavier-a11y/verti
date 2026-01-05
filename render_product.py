import bpy
import math

# Clear default scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import the VertiBand STL
bpy.ops.wm.stl_import(filepath="VertiBand Final.stl")
obj = bpy.context.selected_objects[0]

# Center the object
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
obj.location = (0, 0, 0)

# Add professional material (sleek dark gray with slight metallic)
mat = bpy.data.materials.new(name="VertiBand_Material")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
nodes.clear()

# Add Principled BSDF
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
bsdf.inputs['Base Color'].default_value = (0.08, 0.08, 0.10, 1.0)  # Dark sleek color
bsdf.inputs['Metallic'].default_value = 0.7
bsdf.inputs['Roughness'].default_value = 0.25
bsdf.inputs['Specular IOR Level'].default_value = 0.5

# Material output
output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (200, 0)
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Assign material to object
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)

# Set up camera
bpy.ops.object.camera_add(location=(3, -3, 2))
camera = bpy.context.object
camera.rotation_euler = (math.radians(65), 0, math.radians(45))
bpy.context.scene.camera = camera

# Set up studio lighting (3-point lighting)
# Key light (main light)
bpy.ops.object.light_add(type='AREA', location=(4, -4, 5))
key_light = bpy.context.object
key_light.data.energy = 300
key_light.data.size = 5
key_light.rotation_euler = (math.radians(45), 0, math.radians(45))

# Fill light (softer, opposite side)
bpy.ops.object.light_add(type='AREA', location=(-3, -2, 3))
fill_light = bpy.context.object
fill_light.data.energy = 150
fill_light.data.size = 4

# Rim light (back light for edge definition)
bpy.ops.object.light_add(type='AREA', location=(0, 2, 4))
rim_light = bpy.context.object
rim_light.data.energy = 200
rim_light.data.size = 3

# Set up world background (clean studio)
world = bpy.context.scene.world
world.use_nodes = True
world_nodes = world.node_tree.nodes
world_nodes.clear()

bg = world_nodes.new(type='ShaderNodeBackground')
bg.inputs['Color'].default_value = (0.95, 0.96, 0.98, 1.0)  # Light blue-gray
bg.inputs['Strength'].default_value = 0.8

world_output = world_nodes.new(type='ShaderNodeOutputWorld')
world.node_tree.links.new(bg.outputs['Background'], world_output.inputs['Surface'])

# Render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.cycles.use_denoising = False  # Disable denoiser
scene.render.resolution_x = 2000
scene.render.resolution_y = 2000
scene.render.film_transparent = True
scene.render.filepath = "/home/user/verti/vertiband-render.png"

# Render
bpy.ops.render.render(write_still=True)

print("Render complete: vertiband-render.png")
