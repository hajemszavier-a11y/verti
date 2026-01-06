import bpy
import math

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# First, import the electronics box to see its actual size
bpy.ops.wm.stl_import(filepath="/home/user/verti/VertiBand Final.stl")
box = bpy.context.selected_objects[0]
box.name = "VertiBandBox"

# Scale box to realistic size
box.scale = (0.0008, 0.0008, 0.0008)
box.location = (0, 0, 0)  # Center it first to build headband around it

# Get box dimensions after scaling
bpy.context.view_layer.update()
box_dims = box.dimensions
print(f"Box dimensions: {box_dims}")

# Create headband cylinder appropriate for the box size
# Headband should wrap around head (~22cm diameter) with box at back
headband_radius = 0.11  # ~22cm diameter for average head
band_width = max(0.035, box_dims.y * 1.2)  # Band width based on box width

bpy.ops.mesh.primitive_cylinder_add(
    radius=headband_radius,
    depth=band_width,
    location=(0, 0, 0)
)
outer = bpy.context.object

# Inner cylinder for hollow band
bpy.ops.mesh.primitive_cylinder_add(
    radius=headband_radius - 0.013,  # 1.3cm thick band
    depth=band_width + 0.01,
    location=(0, 0, 0)
)
inner = bpy.context.object

# Boolean to create band
bool_mod = outer.modifiers.new(name="Boolean", type='BOOLEAN')
bool_mod.operation = 'DIFFERENCE'
bool_mod.object = inner
bpy.context.view_layer.objects.active = outer
bpy.ops.object.modifier_apply(modifier="Boolean")
bpy.data.objects.remove(inner, do_unlink=True)

headband = outer
headband.name = "Headband"
headband.rotation_euler = (math.radians(90), 0, 0)

# Black fabric material
fabric_mat = bpy.data.materials.new(name="Fabric")
fabric_mat.use_nodes = True
bsdf = fabric_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1.0)
bsdf.inputs['Roughness'].default_value = 0.95
headband.data.materials.append(fabric_mat)

# Position box at back of headband
box.location = (0, headband_radius - 0.005, -0.005)
box.rotation_euler = (math.radians(90), 0, math.radians(180))

# Tech material for box
tech_mat = bpy.data.materials.new(name="Tech")
tech_mat.use_nodes = True
tech_bsdf = tech_mat.node_tree.nodes["Principled BSDF"]
tech_bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.06, 1.0)
tech_bsdf.inputs['Metallic'].default_value = 0.4
tech_bsdf.inputs['Roughness'].default_value = 0.25
box.data.materials.append(tech_mat)

# Camera - 3/4 view to show box at back
cam = bpy.data.cameras.new("Camera")
cam_obj = bpy.data.objects.new("Camera", cam)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj
cam_obj.location = (0.32, -0.22, 0.18)
cam_obj.rotation_euler = (math.radians(68), 0, math.radians(50))
cam.lens = 70

# Lighting
key = bpy.data.lights.new(name="Key", type='AREA')
key.energy = 400
key.size = 3
key_obj = bpy.data.objects.new("Key", key)
bpy.context.scene.collection.objects.link(key_obj)
key_obj.location = (3, -2.5, 3)
key_obj.rotation_euler = (math.radians(45), 0, math.radians(30))

fill = bpy.data.lights.new(name="Fill", type='AREA')
fill.energy = 150
fill.size = 3
fill_obj = bpy.data.objects.new("Fill", fill)
bpy.context.scene.collection.objects.link(fill_obj)
fill_obj.location = (-2, -2, 2)

rim = bpy.data.lights.new(name="Rim", type='AREA')
rim.energy = 200
rim.size = 2
rim_obj = bpy.data.objects.new("Rim", rim)
bpy.context.scene.collection.objects.link(rim_obj)
rim_obj.location = (-2, 3, 2)

top = bpy.data.lights.new(name="Top", type='AREA')
top.energy = 100
top.size = 4
top_obj = bpy.data.objects.new("Top", top)
bpy.context.scene.collection.objects.link(top_obj)
top_obj.location = (0, 0, 5)

# Render
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 256
scene.cycles.use_denoising = False
scene.render.resolution_x = 2000
scene.render.resolution_y = 2000
scene.render.film_transparent = False
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'High Contrast'

scene.render.filepath = "/home/user/verti/vertiband-headband.png"
bpy.ops.render.render(write_still=True)

print("✓ Done")
