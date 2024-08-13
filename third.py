import trimesh
import numpy as np
import os
from PIL import Image
def rotate_mesh(mesh, angle_x=0, angle_y=0, angle_z=0):
  """Rotates the mesh around the specified axes."""
  rotation_matrix = trimesh.transformations.rotation_matrix(
      radians=np.radians([angle_x, angle_y, angle_z]), deg=False)
  mesh.apply_transform(rotation_matrix)
def load_mesh(file_path):
  """Loads a mesh from the given file path."""
  return trimesh.load(file_path)

def set_material(mesh, texture_path, color=(1.0, 1.0, 1.0)):
  """Assigns a simple material to the mesh with an optional texture and color."""
  if texture_path:
    # Load texture image using PIL
    texture_image = Image.open(texture_path)
    # Create a Trimesh material with texture (implementation may vary)
    material = trimesh.visual.material.SimpleMaterial(image=texture_image)  # Placeholder, check Trimesh documentation for material options
  else:
    material = trimesh.visual.material.SimpleMaterial(color=color)
    mesh.visual = trimesh.visual.TextureVisuals(material=material)  # Assign material to mesh visuals
    return
texture_path = "C:/Users/hafsa/Documents/texturemodule/texture.png"

#visualize_mask(mask)
obj_path="C:/Users/hafsa/Documents/texturemodule/male-5-outdoor_0_bottom.obj"
#mesh = trimesh.load(obj_path, process=False)

output_folder = "C:/Users/hafsa/Documents/texturemodule"
total_frames = 90
radius = 9.0
for i in range(total_frames):
    # Load meshes
    mesh = [load_mesh(obj_path)]

    # Set materials (optional)
  
    set_material(mesh, texture_path)

    # Apply rotations based on frame number (adjust calculation as needed)
    angle = (i / total_frames) * 2 * np.pi
    
    camera_position=rotate_mesh(mesh, angle_z=angle)  # Rotate around Z-axis for circular path

    
    # Set camera position (adjust based on your desired view)
    mesh.visual.camera = trimesh.scene.camera.PinholeCamera(fov=60, focal_point=camera_position)  # Adjust field of view (FOV)

    # Render to image (implementation may vary)
    image = mesh.screenshot(resolution=(175, 350))  # Adjust resolution if needed
    image.save(os.path.join(output_folder, f'im_{i:02}.png'))


