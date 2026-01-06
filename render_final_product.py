import bpy
import math

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create circular headband (torus)
bpy.ops.mesh.primitive_torus_add(
    major_radius=0.11,
    minor_radius=0.015,
    location=(0, 0, 0)
)
headband = bpy.context.object
headband.name = "FabricBand"
headband.rotation_euler = (math.radians(90), 0, 0)

# BLACK FABRIC material
fabric_mat = bpy.data.materials.new(name="Black_Fabric")
fabric_mat.use_nodes = True
bsdf = fabric_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.015, 0.015, 0.015, 1.0)
bsdf.inputs['Roughness'].default_value = 0.95
headband.data.materials.append(fabric_mat)

# Import electronics box
bpy.ops.wm.stl_import(filepath="/home/user/verti/VertiBand Final.stl")
box = bpy.context.selected_objects[0]
box.name = "ElectronicsBox"

# Scale and position box at the back inside the headband
box.scale = (0.0007, 0.0007, 0.0007)
box.location = (0, 0.095, 0)
box.rotation_euler = (math.radians(90), 0, 0)

# Dark tech material for electronics box
tech_mat = bpy.data.materials.new(name="Dark_Tech")
tech_mat.use_nodes = True
tech_bsdf = tech_mat.node_tree.nodes["Principled BSDF"]
tech_bsdf.inputs['Base Color'].default_value = (0.08, 0.08, 0.09, 1.0)
tech_bsdf.inputs['Metallic'].default_value = 0.6
tech_bsdf.inputs['Roughness'].default_value = 0.2
box.data.materials.append(tech_mat)

# Camera setup - angled to show both headband and box
cam = bpy.data.cameras.new("Camera")
cam_obj = bpy.data.objects.new("Camera", cam)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Position camera at 45-degree angle to show the back where box is
cam_obj.location = (0.25, -0.2, 0.12)
cam_obj.rotation_euler = (math.radians(75), 0, math.radians(50))
cam.lens = 85

# Professional studio lighting
# Key light
key_light = bpy.data.lights.new(name="Key", type='AREA')
key_light.energy = 300
key_light.size = 2
key_obj = bpy.data.objects.new("Key", key_light)
bpy.context.scene.collection.objects.link(key_obj)
key_obj.location = (2, -1.5, 2)
key_obj.rotation_euler = (math.radians(45), 0, math.radians(30))

# Fill light
fill_light = bpy.data.lights.new(name="Fill", type='AREA')
fill_light.energy = 150
fill_light.size = 2
fill_obj = bpy.data.objects.new("Fill", fill_light)
bpy.context.scene.collection.objects.link(fill_obj)
fill_obj.location = (-1.5, -1, 1.5)

# Rim light
rim_light = bpy.data.lights.new(name="Rim", type='AREA')
rim_light.energy = 200
rim_light.size = 1
rim_obj = bpy.data.objects.new("Rim", rim_light)
bpy.context.scene.collection.objects.link(rim_obj)
rim_obj.location = (-1, 2, 1)

# Top light
top_light = bpy.data.lights.new(name="Top", type='AREA')
top_light.energy = 100
top_light.size = 3
top_obj = bpy.data.objects.new("Top", top_light)
bpy.context.scene.collection.objects.link(top_obj)
top_obj.location = (0, 0, 3)
top_obj.rotation_euler = (0, 0, 0)

# Render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 200
scene.cycles.use_denoising = False
scene.render.resolution_x = 1800
scene.render.resolution_y = 1800
scene.render.film_transparent = False
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium High Contrast'

# Render
scene.render.filepath = "/home/user/verti/vertiband-product-final.png"
bpy.ops.render.render(write_still=True)

print("Render complete!")
