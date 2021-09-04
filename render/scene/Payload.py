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

class Payload:  
  @classmethod
  def setup(cls) :

    tag = 'Payload: setup'

    ## Create Payload
    ## ------------------------------------------------
    # Create blender mesh
    filename = Get.config(
      'runtime/scene/geometry/name'
    )
    name     = Get.fmt('payload', **Get.mesh_keys)
    mesh     = D.meshes.new(name)
    lg.info(f'{tag}: mesh: {mesh.name}')

    cls.mesh_load(mesh, filename)
    cls.mesh_standardize(mesh)

    # Create payload object
    name = Get.fmt('payload', **Get.obj_keys)
    payload = D.objects.new(name, mesh)
    lg.info(f'{tag}: object: {payload.name}')

    # Add payload object to collection
    for collection in Get.collections() :
      collection.objects.link(payload)
      lg.info(f'{tag}: collection: {collection.name}')

    # # UV Unwrap
    # assign_dummy_material_to_payload(id)
    # smart_uv_unwrap(Get.payload(COLL.S, id), id)

  @classmethod
  def mesh_load(
      cls, data, filename,
      import_axes=None
  ) :
    import bmesh
    from pathlib import Path

    tag = '{}: load_mesh'.format(
      cls.__name__
    )

    prefix    = (
      Path(Get.config('geometry/prefix'))
    )
    import_mesh = Op.import_scene.stl
    im_args     = {}

    if filename.endswith('obj') :
      # import as obj
      # -----------------------------------
      import_mesh = Op.import_scene.obj

      try :
        fwd, up = (
          (
            type(import_axes) in (list, tuple)
            and
            import_axes
          )
          or
          (
            type(import_axes) is str
            and
            Get.config(import_axes)
          )
          or
          Get.config(
          'geometry/import_axes'
          )
        )
      except LookupError as e :
        lg.warning(f'{tag}: config: `geometry/'
                   f'import_axes\' not defined')

        fwd, up = ('-Z', 'Y')

      im_args.update({
        "axis_forward" : fwd,
        "axis_up"      : up,
      })

    elif filename.endswith('stl') :
      # load as stl
      # -----------------------------------
      import_mesh = Op.import_mesh.stl

    else :
      ## geometry not recognized
      raise ValueError(
        f'{tag}: UNSUPPORTED: {filename}'
      )

    lg.info(f'{tag}: from path prefix: {prefix}')
    lg.info(
      f'{tag}: filename: {filename}, args: {im_args}'
    )

    import_file = (
      filename
      if filename.startswith('/')
      else str(prefix/filename)
    )
    import_mesh(
      filepath = import_file,
      **im_args
    )
    imported = C.selected_objects[0]

    ## Freeze transforms
    Op.object.transform_apply({
      'selected_objects': [imported],
      'object': imported,
    },
      location=True, rotation=True, scale=True
    )

    bm = bmesh.new()
    bm.from_mesh(imported.data)
    Op.object.delete({
      'selected_objects': [imported]
    })
    lg.info(f'{tag}: Freeze transforms ...done')

    bm.to_mesh(data)
    bm.free()

  @classmethod
  def mesh_standardize(cls, data) :
    import bmesh
    import numpy as np
    from functools import reduce
    import operator as op
    from random import random

    V = M.Vector

    tag = '{}: mesh_standardize'.format(
      cls.__name__
    )

    bm = bmesh.new()
    bm.from_mesh(data)

    ## Translation
    ## --------------------------------------------------
    # Compute translation
    eps = 1e-3
    verts = np.array([list(v.co) for v in bm.verts])
    vmin, vmax = V(verts.min(0)), V(verts.max(0))
    vmid = vmin.copy()
    vmid.xy = 0.5 * (vmin.xy + vmax.xy)
    _goto = -vmid
    _goto.z += eps

    # Translate
    bmesh.ops.translate(
      bm,
      verts=bm.verts,
      vec=_goto
    )
    lg.info(f'{tag}: Translating to: {_goto} ...done')

    ## Scale
    ## --------------------------------------------------
    
    max_cu = Get.config('geometry/max_cu')
    max_bb = Get.config('geometry/max_bb')
    min_scale = Get.config('geometry/min_scale')

    rnd = lambda x0,x1: x0 + (x1 - x0) * random()

    # Make the volume close to MAX_CU cunits, but dont
    # scale any bounding box component more than MAX_BB
    # units. Finally scale down by a factor uniformly
    # sampled to a min value of MIN_SCALE.
    cu_fac = (
      (
        max_cu
        /
        reduce(op.mul, vmax - vmin)
      )
      ** (1./3)
    )
    bb_fac = (
      max_bb
      /
      max(vmax - vmin)
    )
    r_fac = rnd(min_scale, 1)

    f = min(cu_fac, bb_fac) * r_fac
    _fac = [f, f, f]

    bmesh.ops.scale(
      bm,
      verts=bm.verts,
      vec=_fac
    )
    lg.info(f'{tag}: Scaling by: {_fac} ...done')

    bm.to_mesh(data)
    bm.free()
