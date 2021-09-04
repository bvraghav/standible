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

class CameraGnomon:
  @staticmethod
  def setup() :
    scene = Get.scene()

    tag = 'CameraGnomon: setup'
    lg.info(f'{tag}: scene: {scene.name}')

    ## Create Gnomon Camera (orthographic from top)
    ## --------------------------------------------------
    name = Get.fmt('g_camera')
    data = D.cameras.new(name)
    camera = D.objects.new(name, data)

    ## Link to scene and activate
    scene.collection.objects.link(camera)
    scene.camera = camera

    ## Freeze camera pose
    camera.matrix_world.translation = M.Vector(
      Get.config('gnomon_camera/location')
    )
    camera.rotation_euler = M.Euler(
      Get.config('gnomon_camera/orientation/euler')
    )

    ## Set camera attributes
    Set.attributes_from_config(
      bpy_object = camera.data,
      config = Get.config('gnomon_camera/blender'),
    )

    lg.info(
      f'{tag}: Object:{scene.camera.name} '
      f'Data:{scene.camera.data.name}'
    )



