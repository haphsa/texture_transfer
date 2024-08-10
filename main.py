import numpy as np
from PIL import Image
import trimesh
import re

def obj_to_off(obj_data):
  """Converts OBJ file content to OFF format.

  Args:
    obj_data: The content of the OBJ file as a string.

  Returns:
    The content of the OFF file as a string.
  """

  vertices = []
  faces = []

  for line in obj_data.splitlines():
    if line.startswith('v '):
      coords = line[2:].split()
      vertices.append(coords)
    elif line.startswith('f '):
      face_vertices = line[2:].split()
      face = [int(v.split('/')[0]) - 1 for v in face_vertices]  # Assuming vertex index only
      faces.append(face)

  num_vertices = len(vertices)
  num_faces = len(faces)
  num_edges = (num_faces * 3)  # Assuming triangular faces

  off_content = f"OFF {num_vertices} {num_faces} {num_edges}\n"
  for vertex in vertices:
    off_content += ' '.join(vertex) + '\n'
  for face in faces:
    off_content += f"{len(face)} {' '.join(str(v) for v in face)}\n"

  return off_content

def transfer_texture(obj_path, texture_path):

    mesh = trimesh.load(obj_path, process=False)

    texture_image = Image.open(texture_path)
    texture_data = np.array(texture_image)
   

    im = texture_image
    m = mesh

    #tex = trimesh.visual.TextureVisuals(image=im)
    #m.visual.texture = tex


    uv = np.random.rand(m.vertices.shape[0], 2)

    material = trimesh.visual.texture.SimpleMaterial(image=im)
    color_visuals = trimesh.visual.TextureVisuals(uv=uv, image=im, material=material)
    mesh=trimesh.Trimesh(vertices=m.vertices, faces=m.faces, visual=color_visuals, validate=True, process=False)
    #mesh.show
    # Extract UV coordinates from mesh
    #uvs = mesh.visual.uv

    # ... (logic to map UV coordinates to pixel coordinates)

    # ... (logic to transfer pixel data to mesh vertices)

    # Save or display the textured mesh
    # mesh.export('textured_model.obj')
    # mesh.show()  # Using trimesh viewer

    return mesh

def generate_mask(image_path):

  img = Image.open(image_path)
  img_array = np.array(img)
  if img_array.shape[2] == 4:
    alpha_channel = img_array[:, :, 3]
    mask = alpha_channel > 0
  else:
    
    mask = np.ones(img_array.shape[:2], dtype=bool)

  return mask

def visualize_mask(mask):
  
  mask_img = Image.fromarray(mask * 255).convert('L')
  mask_img.show()

image_path = "C:/Users/hafsa/Documents/texturemodule/texture.png"
mask = generate_mask(image_path)
#visualize_mask(mask)
obj_path="C:/Users/hafsa/Documents/texturemodule/male-5-outdoor_0_bottom.obj"
mesh = trimesh.load(obj_path, process=False)

result=transfer_texture(obj_path,image_path)
result.show()