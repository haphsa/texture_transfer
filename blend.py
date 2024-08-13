import trimesh.viewer as trimeshv
import numpy as np
from PIL import Image

import trimesh
import re


def transfer_texture(obj_path, texture_path):

    #mesh = trimesh.load(obj_path, process=False)
    mesh = trimesh.load(obj_path, process=False)

    texture_image = Image.open(texture_path)
    texture_data = np.array(texture_image)
   

    im = texture_image
    uv = np.random.rand(mesh.vertices.shape[0], 2)
    
    material = trimesh.visual.texture.SimpleMaterial(image=im)
    color_visuals = trimesh.visual.TextureVisuals(uv=uv, image=im, material=material)
    mesh.visual = color_visuals
    mesh.export(file_obj='model3.obj')

    mesh.show()
    return 

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

image_path = "C:/Users/hafsa/Documents/texturemodule/tryout.jpg"
mask = generate_mask(image_path)
#visualize_mask(mask)
obj_path="C:/Users/hafsa/Documents/texturemodule/male-5-outdoor_0_bottom.ply"
mesh = trimesh.load(obj_path, process=False)

transfer_texture(obj_path,image_path)
