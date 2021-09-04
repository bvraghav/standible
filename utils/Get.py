import logging as lg
from pathlib import Path

# import bpy
# from bpy import (
#   context as C, data as D, ops as Op)
# import mathutils as M, math as m

import math as m

from . config import get_config
from . xchange import ns

bpy, C, D, M = [None] * 4

class Get :
  mesh_keys = {
    'geom': 'Mesh',
  }

  obj_keys = {
    'geom': 'Obj',
  }
 
  @classmethod
  def config(cls, key_path=None, mod_bpy=None, mod_mathutils=None) :

    if mod_bpy :
      global bpy, C, D
      bpy = mod_bpy
      C = bpy.context
      D = bpy.data

    if mod_mathutils :
      global M
      M = mod_mathutils

    config = get_config()
    if key_path :
      from functools import reduce
      from operator import getitem

      config = reduce(
        getitem,
        key_path.split('/'),
        config
      )

    return config

  @classmethod
  def fmt(cls, key=None, **kwargs) :
    fmt = cls.config('fmt')
    
    if key :
      fmt = fmt.get(key)

    if kwargs :
      fmt = fmt.format(**kwargs)

    return fmt

  @classmethod
  def runtime(cls, key) :
    return cls.config(f'runtime/{key}')

  @classmethod
  def scene(cls) :
    return D.scenes[cls.fmt('scene')]

  @classmethod
  def world(cls):
    return D.worlds.get(cls.fmt('world'))

  @classmethod
  def view(cls, name = None) :
    view_layers = cls.scene().view_layers
    name = name or Get.config(f'runtime/style')
    return view_layers[cls.fmt(
      'view',
      name=Get.config(f'views/{name}/name')
    )]

  @classmethod
  def collections(cls, name=None) :
    collection_keys = (
      cls.view(name)
      .layer_collection
      .children
      .keys()
    )

    return [
      cls.collection(cl)
      for cl in collection_keys
    ]

  @classmethod
  def collection_kv(cls, name=None) :
    name = name or Get.config(f'runtime/style')
    key = f'collections/{name}/name'
    suffix = ''
    try :
      name = cls.fmt(
        'collection',
        name=Get.config(key)
      )
    except KeyError as e :
      # If name not in config.json, try the nascent
      # name instead
      lg.warning(
        f'Get: collection: name: {key} not in config.'
      )
      suffix = ' instead'

    lg.info(f'Get: collection: Using key:{name}{suffix}.')
    return name, D.collections.get(name)

  @classmethod
  def collection(cls, name=None) :
    _, collection = cls.collection_kv(name)
    return collection

  @classmethod
  def fmt_collection(cls, name=None) :
    name, _ = cls.collection_kv(name)
    return name

  @classmethod
  def light(cls) :
    return D.objects[cls.fmt('light')]

  @classmethod
  def camera(cls) :
    return D.objects[cls.fmt('camera')]

  @classmethod
  def gnomon_camera(cls) :
    return D.objects[cls.fmt('g_camera')]

  @classmethod
  def mesh(cls, key) :
    return D.meshes.get(
      cls.fmt(key, **cls.mesh_keys)
    )

  @classmethod
  def bpy_object(cls, key) :
    return D.objects.get(
      cls.fmt(key, **cls.obj_keys)
    )

  @classmethod
  def plane(cls) :
    return cls.bpy_object('plane')

  @classmethod
  def plane_mesh(cls) :
    return cls.mesh('plane')

  @classmethod
  def payload(cls) :
    return cls.bpy_object('payload')

  @classmethod
  def payload_mesh(cls) :
    return cls.mesh('payload')

  @classmethod
  def gnomon(cls) :
    return cls.bpy_object('gnomon')

  @classmethod
  def gnomon_mesh(cls) :
    return cls.mesh('gnomon')

  @classmethod
  def mat_kv(cls, name) :
    key = f'materials/{name}/name'
    suffix = ''
    try :
      name = cls.fmt(
        'material',
        name = Get.config(key)
      )
    except LookupError as e :
      # If name not in config.json, try the nascent
      # name instead
      lg.warning(
        f'Get: mat_kv: name: {key} not in config.'
      )
      suffix = ' instead'

    lg.info(f'Get: mat_kv: Using key:{name}{suffix}.')
    return name, D.materials.get(name)

  @classmethod
  def mat(cls, name) :
    _, mat = cls.mat_kv(name)
    return mat

  @classmethod
  def fmt_mat(cls, name) :
    name, _ = cls.mat_kv(name)
    return name

  @classmethod
  def texture(cls, path, tone, load_fn=None) :
    txr_name = cls.fmt(
      'texture',
      basename=Path(path).name,
      tone=tone,
    )
    txr = D.images.get(txr_name)

    if not txr :
      txr = load_fn(path, tone, txr_name)

    return txr

  @classmethod
  def lineset_kv(cls, style=None) :
    try :

      style = style or Get.runtime('style')
      name = Get.config(f'views/{style}/name')
    
    except LookupError as e:
      name = style

    return [name, (
      cls.view(style)
      .freestyle_settings
      .linesets
      .get(
        cls.fmt('lineset', name=name)
      )
    )]

  @classmethod
  def fmt_lineset(cls, name=None) :
    name, _ = cls.lineset_kv(name)
    return name

  @classmethod
  def lineset(cls, name=None) :
    _, result = cls.lineset_kv(name)
    return result

  @classmethod
  def linestyle(cls) :
    return D.linestyles.get(
      cls.fmt('linestyle')
    )

  @classmethod
  def node_group(cls, name) :
    return D.node_groups.get(
      cls.fmt('node_group', name=name)
    )

  @classmethod
  def output(cls, **kwargs) :
    return cls.fmt('output', **kwargs)
