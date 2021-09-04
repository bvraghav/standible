import logging as lg

from utils import Get, Set

import bpy
from bpy import (
  context as C,
  data as D,
  ops as Op
)

import math as m
import mathutils as M

class Camera:
  @staticmethod
  def setup() :
    scene = Get.scene()

    tag = 'Camera: setup'
    lg.info(f'{tag}: scene: {scene.name}')

    ## Create Camera
    ## ------------------------------------------------

    # Add as object, an to scene
    name = Get.fmt('camera')
    data = D.cameras.new(name)  # Create camera
    camera = D.objects.new(name, data) # Create object
    scene.collection.objects.link(camera) # Link to
                                          # scene
                                          # collection

    # Set active camera for scene
    scene.camera = camera       # Set as active

    Set.attributes_from_config(
      bpy_object = camera.data,
      config = Get.config('camera/blender'),
    )

    lg.info(
      f'{tag}: Object:{scene.camera.name} '
      f'Data:{scene.camera.data.name}'
    )
