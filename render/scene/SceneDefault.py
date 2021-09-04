import logging as lg

import bpy
from bpy import (
  context as C,
  data as D,
  ops as Op
)

import math as m
import mathutils as M

from utils import Get, Set, hex_to_color

from . Taxonomy import Taxonomy
from . Camera import Camera
from . Light import Light
from . Plane import Plane
from . Payload import Payload
from . Render import Render
# from . Materials import Materials

class SceneDefault :
## ====================================================

  def __init__(self, config, data) :
    self.config = config

    # Read ndjson data. 
    data = (
      self.read_data_may_be(data)
      .pop(0)
    )

    # Save as runtime config
    Set.runtime('scene', data)

  def setup(self) :
    lg.debug(
      'Setting up scene from data: %s',
      Get.config('runtime/scene')
    )

    self.clear_scene()

    Taxonomy().setup()
    Camera.setup()
    Light.setup()
    Plane.setup()
    Payload.setup()
    Render.setup()
    # Materials.setup()

  @classmethod
  def read_data_may_be(cls, data) :
    from pathlib import Path
    from utils import read_ndjson

    if type(data) is str or isinstance(data, Path) :
      data = read_ndjson(data)

    return data

  def clear_scene(self) :
    tag = '{}: clear_scene'.format(
      self.__class__.__name__
    )

    try :
      scene = Get.scene()
      lg.info(f'{tag}: scene: {scene.name}')

      for c in scene.collection.children.keys() :
        collection = D.collections[c]

        objs = collection.objects.keys()
        objs = list(map(
          lambda k: D.objects[k],
          objs
        ))
        obj_names = list(map(
          lambda obj: obj.name,
          objs
        ))
        Op.object.delete({
          'selected_objects': objs
        })
        lg.info(
          f'{tag}: objects:{obj_names} C:{c}'
        )

        scene.collection.children.unlink(collection)
        lg.info(f'{tag}: collection: {c}')

      if len(D.scenes) == 1 :
        D.scenes.new('Dummy')

      D.scenes.remove(scene)

    except LookupError as e :
      pass

    world = Get.world()
    if world :
      lg.info(f'{tag}: world: {world.name}')
      D.worlds.remove(world)

    style = Get.config('runtime/style')
    for c in (
        Get.config(f'views/{style}/collections')
    ) :
      collection = Get.collection(c)
      if collection : 
        D.collections.remove(collection)
