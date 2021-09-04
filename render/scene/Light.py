import logging as lg

from utils import Get, Set, hex_to_color

import bpy
from bpy import (
  context as C,
  data as D,
  ops as Op
)

import math as m
import mathutils as M

class Light:    
  def setup() :
    scene = Get.scene()

    tag = 'Light setup'
    lg.info(f'{tag}: scene: {scene.name}')

    ## Create Light
    ## ------------------------------------------------
    # Add as object, and to scene
    name = Get.fmt('light')
    data = D.lights.new(name, 'AREA')
    light = D.objects.new(name, data)
    scene.collection.objects.link(light)

    ## Convert and Assign Color
    color = Get.config('light/blender/color')
    color = hex_to_color(color)
    light.data.color = color
    
    ## Assign other settings
    Set.attributes_from_config (
      bpy_object = light.data,
      config = Get.config('light/blender'),
      excludes = ['color']
    )

    lg.info(
      f'{tag}: Object:{light.name} '
      f'Data:{light.data.name}'
    )
