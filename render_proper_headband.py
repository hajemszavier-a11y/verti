import bpy
import math

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create THIN FLAT headband like Nike/athletic bands
# Using a curve to create a ribbon-like band
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.11,
    depth=0.04,  # Width of the band (thin, not thick)
    location=(0, 0, 0)
)
outer_cylinder = bpy.context.object

# Create inner cylinder to subtract
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.097,  # Slightly smaller to create thin band
    depth=0.05,
    location=(0, 0, 0)
)
inner_cylinder = bpy.context.object

# Boolean modifier to create hollow band
bool_mod = outer_cylinder.modifiers.new(name="Boolean", type='BOOLEAN')
bool_mod.operation = 'DIFFERENCE'
bool_mod.object = inner_cylinder
bpy.context.view_layer.objects.active = outer_cylinder
bpy.ops.object.modifier_apply(modifier="Boolean")

# Delete inner cylinder
bpy.data.objects.remove(inner_cylinder, do_unlink=True)

headband = outer_cylinder
headband.name = "FabricHeadband"
headband.rotation_euler = (math.radians(90), 0, 0)

# BLACK FABRIC material - matte, soft
fabric_mat = bpy.data.materials.new(name="Black_Fabric")
fabric_mat.use_nodes = True
bsdf = fabric_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1.0)  # Deep black
bsdf.inputs['Roughness'].default_value = 0.98  # Very matte fabric
bsdf.inputs['Sheen'].default_value = 0.3  # Slight fabric sheen
headband.data.materials.append(fabric_mat)

# Import electronics box - the actual VertiBand component
bpy.ops.wm.stl_import(filepath="/home/user/verti/VertiBand Final.stl")
box = bpy.context.selected_objects[0]
box.name = "VertiBandBox"

# Scale box to realistic size
box.scale = (0.0008, 0.0008, 0.0008)

# Position at BACK of headband (occipital area)
# Y positive is back, needs to be touching/integrated with the band
box.location = (0, 0.105, -0.01)  # At the back, slightly lower
box.rotation_euler = (math.radians(90), 0, math.radians(180))

# Dark tech plastic material for electronics housing
tech_mat = bpy.data.materials.new(name="Tech_Plastic")
tech_mat.use_nodes = True
tech_bsdf = tech_mat.node_tree.nodes["Principled BSDF"]
tech_bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.06, 1.0)  # Dark gray
tech_bsdf.inputs['Metallic'].default_value = 0.3
tech_bsdf.inputs['Roughness'].default_value = 0.3
tech_bsdf.inputs['Specular'].default_value = 0.5
box.data.materials.append(tech_mat)

# Camera - positioned to show the complete headband with box at back
cam = bpy.data.cameras.new("Camera")
cam_obj = bpy.data.objects.new("Camera", cam)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# 3/4 view angle to see both front of headband and box at back
cam_obj.location = (0.28, -0.18, 0.15)
cam_obj.rotation_euler = (math.radians(70), 0, math.radians(55))
cam.lens = 75

# Professional product lighting
# Key light - main light source
key_light = bpy.data.lights.new(name="Key", type='AREA')
key_light.energy = 350
key_light.size = 2.5
key_obj = bpy.data.objects.new("Key", key_light)
bpy.context.scene.collection.objects.link(key_obj)
key_obj.location = (2.5, -2, 2.5)
key_obj.rotation_euler = (math.radians(50), 0, math.radians(35))

# Fill light - soften shadows
fill_light = bpy.data.lights.new(name="Fill", type='AREA')
fill_light.energy = 120
fill_light.size = 3
fill_obj = bpy.data.objects.new("Fill", fill_light)
bpy.context.scene.collection.objects.link(fill_obj)
fill_obj.location = (-2, -1.5, 1.8)

# Back rim light - separate product from background
rim_light = bpy.data.lights.new(name="Rim", type='AREA')
rim_light.energy = 180
rim_light.size = 1.5
rim_obj = bpy.data.objects.new("Rim", rim_light)
bpy.context.scene.collection.objects.link(rim_obj)
rim_obj.location = (-1.5, 2.5, 1.5)

# Top light - overall ambient
top_light = bpy.data.lights.new(name="Top", type='AREA')
top_light.energy = 80
top_light.size = 4
top_obj = bpy.data.objects.new("Top", top_light)
bpy.context.scene.collection.objects.link(top_obj)
top_obj.location = (0, 0, 4)

# Render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 256
scene.cycles.use_denoising = False
scene.render.resolution_x = 2000
scene.render.resolution_y = 2000
scene.render.film_transparent = False
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'High Contrast'

# Output
scene.render.filepath = "/home/user/verti/vertiband-proper.png"
bpy.ops.render.render(write_still=True)

print("✓ Proper headband render complete")
