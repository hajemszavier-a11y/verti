import bpy
import math

# Clear default scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import all three STL components
# Main headband
bpy.ops.wm.stl_import(filepath="VertiBand Final.stl")
headband = bpy.context.selected_objects[0]
headband.name = "Headband"

# Head support (back of head)
bpy.ops.wm.stl_import(filepath="VertiBand Head Support Final.stl")
head_support = bpy.context.selected_objects[0]
head_support.name = "HeadSupport"

# Electronics case
bpy.ops.wm.stl_import(filepath="VertiBand Case Final.stl")
case = bpy.context.selected_objects[0]
case.name = "Case"

# Center everything
for obj in [headband, head_support, case]:
    obj.select_set(True)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
bpy.context.view_layer.objects.active = headband
bpy.ops.object.location_clear()

# BLACK FABRIC MATERIAL for headband and head support (like sweatband)
fabric_mat = bpy.data.materials.new(name="Black_Fabric")
fabric_mat.use_nodes = True
nodes = fabric_mat.node_tree.nodes
links = fabric_mat.node_tree.links
nodes.clear()

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)  # Deep black
bsdf.inputs['Metallic'].default_value = 0.0  # No metallic (fabric)
bsdf.inputs['Roughness'].default_value = 0.85  # Rough fabric texture
bsdf.inputs['Specular IOR Level'].default_value = 0.3  # Low specular

output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (200, 0)
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Assign fabric material to headband and head support
for obj in [headband, head_support]:
    if obj.data.materials:
        obj.data.materials[0] = fabric_mat
    else:
        obj.data.materials.append(fabric_mat)

# DARK GRAY PLASTIC for electronics case (professional tech look)
plastic_mat = bpy.data.materials.new(name="Dark_Plastic")
plastic_mat.use_nodes = True
nodes = plastic_mat.node_tree.nodes
links = plastic_mat.node_tree.links
nodes.clear()

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
bsdf.inputs['Base Color'].default_value = (0.12, 0.12, 0.14, 1.0)  # Dark gray
bsdf.inputs['Metallic'].default_value = 0.1
bsdf.inputs['Roughness'].default_value = 0.4  # Smooth plastic
bsdf.inputs['Specular IOR Level'].default_value = 0.5

output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (200, 0)
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Assign plastic material to case
if case.data.materials:
    case.data.materials[0] = plastic_mat
else:
    case.data.materials.append(plastic_mat)

# Set up camera (better angle to show all components)
bpy.ops.object.camera_add(location=(4, -4, 2.5))
camera = bpy.context.object
camera.rotation_euler = (math.radians(70), 0, math.radians(45))
bpy.context.scene.camera = camera

# Studio lighting setup (professional product photography)
# Key light (main, front-right)
bpy.ops.object.light_add(type='AREA', location=(5, -4, 6))
key_light = bpy.context.object
key_light.data.energy = 400
key_light.data.size = 6
key_light.rotation_euler = (math.radians(50), 0, math.radians(40))

# Fill light (left side, softer)
bpy.ops.object.light_add(type='AREA', location=(-4, -3, 4))
fill_light = bpy.context.object
fill_light.data.energy = 200
fill_light.data.size = 5

# Rim light (back-top for edge definition)
bpy.ops.object.light_add(type='AREA', location=(0, 3, 5))
rim_light = bpy.context.object
rim_light.data.energy = 250
rim_light.data.size = 4

# Top light (soft fill from above)
bpy.ops.object.light_add(type='AREA', location=(0, 0, 7))
top_light = bpy.context.object
top_light.data.energy = 150
top_light.data.size = 8

# World background (clean white studio)
world = bpy.context.scene.world
world.use_nodes = True
world_nodes = world.node_tree.nodes
world_nodes.clear()

bg = world_nodes.new(type='ShaderNodeBackground')
bg.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)  # Pure white
bg.inputs['Strength'].default_value = 1.0

world_output = world_nodes.new(type='ShaderNodeOutputWorld')
world.node_tree.links.new(bg.outputs['Background'], world_output.inputs['Surface'])

# Render settings (high quality)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 256  # Higher quality
scene.cycles.use_denoising = False
scene.render.resolution_x = 2400
scene.render.resolution_y = 2400
scene.render.film_transparent = False  # White background instead of transparent
scene.render.filepath = "/home/user/verti/vertiband-render-v2.png"

# Render
bpy.ops.render.render(write_still=True)

print("Professional render complete: vertiband-render-v2.png")
