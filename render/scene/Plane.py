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

class Plane :
  @classmethod
  def setup(cls) :
    collection = Get.collection()

    tag = 'Plane: setup'

    ## Create Base Plane Mesh
    ## ------------------------------------------------
    # Create blender mesh
    name = Get.fmt('plane', **Get.mesh_keys)
    data = D.meshes.new(name)
    scale = Get.config('plane/scale')
    cls.create_plane_mesh(data, scale)
    lg.info(f'{tag}: mesh: {data.name}')

    # Create mesh object
    name = Get.fmt('plane', **Get.obj_keys)
    plane = D.objects.new(name, data)
    lg.info(f'{tag}: object: {plane.name}')

    # Add mesh object to collection
    collection.objects.link(plane)
    lg.info(f'{tag}: collection: {collection.name}')

    # # TODO: 
    # # UV Unwrap
    # (
    #   assign_material()
    #   and
    #   smart_uv_unwrap()
    # )

  @classmethod
  def create_plane_mesh(cls, data, scale=1) :
    ## Create a BMesh and replace bpy mesh
    ## ------------------------------------------------
    import bmesh
    bm = bmesh.new()

    # Create plane
    bmesh.ops.create_grid(bm,
                          x_segments=1,
                          y_segments=1,
                          size=1,
                          calc_uvs=True)

    # Scale by some constant
    if scale != 1 :
      f = scale
      bmesh.ops.scale(bm, vec=M.Vector((f,f,f)),
                      verts=bm.verts)

    # Replace bpy mesh
    bm.to_mesh(data)

    # Free up bmesh
    bm.free()
    ## ------------------------------------------------
