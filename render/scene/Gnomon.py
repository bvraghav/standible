import logging as lg
from pathlib import Path

from utils import Get, Set

import bpy
from bpy import (
  context as C,
  data as D,
  ops as Op
)

import math as m
import mathutils as M

from . Payload import Payload

class Gnomon(Payload):  
  @classmethod
  def setup(cls) :
    tag = 'Gnomon: setup'

    ## Create Payload
    ## ------------------------------------------------
    # Create blender mesh
    filename = Get.config(
      'gnomon/geometry'
    )
    if filename.startswith("./") :
      configpath = Get.runtime('configpath')
      lg.debug(f'{tag}: configpath: {configpath}')
      filename = str(
        Path(configpath).parent
        /
        filename.replace("./", "")
      )

    name     = Get.fmt('gnomon', **Get.mesh_keys)
    mesh     = D.meshes.new(name)
    lg.info(f'{tag}: mesh: {mesh.name}')

    cls.mesh_load(
      mesh,
      filename,
      import_axes='gnomon/import_axes',
    )

    # Create gnomon object
    name = Get.fmt('gnomon', **Get.obj_keys)
    gnomon = D.objects.new(name, mesh)
    lg.info(f'{tag}: object: {gnomon.name}')

    # Add gnomon object to collection
    for collection in Get.collections() :
      collection.objects.link(gnomon)
      lg.info(f'{tag}: collection: {collection.name}')
