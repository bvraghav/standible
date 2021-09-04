import logging as lg
from pathlib import Path

from utils import Get, Set

import bpy
from bpy import (
  context as C,
  data    as D,
  ops     as Op
)

import mathutils as M
import math as m

class Textures :
  @classmethod
  def setup(cls) :
    from functools import reduce
    from operator import concat

    tag = 'Textures: setup'

    lg.info(f'{tag}')

    prefix = Get.config(
      'textures/prefix'
    )
    name = Get.config(
      'runtime/scene/texture/name'
    )
    path = (Path(prefix) / name)

    origins = Get.config(
      'runtime/scene/texture/origins'
    )

    style = Get.config('runtime/style')
    materials = Get.config(
      f'collections/{style}/materials'
    )
    materials = list(map(
      lambda m: Get.config(
        f'materials/{m}'
      ),
      list(materials.values())
    ))
    
    lg.debug(f'{tag}: materials: {materials}')

    textures = reduce(concat, [
      mat['textures']
      for mat in materials
      if 'textures' in mat
    ], [])

    lg.debug(f'{tag}: textures: {textures}')

    # extract group, mat, node, tone
    from collections import OrderedDict
    extract = lambda txr : [
      txr, *list(
        OrderedDict(sorted(
          Get.config(
            f'textures/image_mapping/{txr}'
          )
          .items()
        ))
        .values()
      )
    ]
    textures = map(extract, textures)

    for (name, group, mat, node, tone) in textures :
      cls.assign(
        path, group, mat, node, tone
      )

      cls.assign_origin(
        origins[name], group, mat
      )

  @classmethod
  def assign(
      cls, prefix, group, mat, node, tone
  ) :
    tag = 'Textures: assign'

    # Get node group
    group = Get.node_group(group)
    if not group :
      group = cls.dup_mat_group(mat, node, group)

    # Update node group texture image
    im_node = group.nodes[Get.config(
      'textures/image_node_name'
    )]
    im_node.image = Get.texture(
      prefix, tone, cls.load
    )
    lg.debug(
      f'{tag}: {mat}:{node}:{group.name}:{tone} '
      f'{im_node.name} <--> {im_node.image.name}'
    )

  @classmethod
  def assign_origin(
      cls, origin, group, mat
  ) :
    tag = 'Textures: assign_origin'

    # Get node group
    mat = Get.mat(mat)
    group = Get.node_group(group)

    # Shift texture origin
    nd = group.nodes[Get.config(
      f'textures/origin_node_name'
    )]

    origin = M.Vector(origin)
    nd.inputs['Location'].default_value = origin

    lg.debug(f'{tag}: {mat.name}:{group.name} '
             f' -> ({origin.x:03f}, {origin.y:03f}, '
             f'{origin.z:03f})')

  @classmethod
  def dup_mat_group(
      cls, mat, node, group
  ) :
    tag = 'Textures: dup_mat_group'

    # Get mat and group
    mat = Get.mat(mat)
    group = Get.node_group(group)
    if not group :
      group = cls.dup_group(group)

    # Update node group
    node = mat.node_tree.nodes[node]
    node.node_tree = group

    lg.info(f'{tag}: assign {mat.name}:{node.name} '
             '-> {group.name}')

    return group

  @classmethod
  def dup_group(cls, name) :
    tag = 'Textures: dup_group'

    # Copy node group with scene id
    style = Get.config('runtime/style')
    group = D.node_groups[name].copy()
    group.name = Get.fmt(
      'node_group',
      name=f'{style}.{name}'
    )

    lg.info(f'{tag}: {name}->{group.name}')
    return group
  
  @classmethod
  def load(cls, prefix, tone, name) :
    tag = 'Textures: load'

    filename = str(Path(prefix) / f'{tone}.png')
    txr = D.images.load(filename)
    txr.name = name

    lg.info(f'{tag}: {name} <- ({prefix}/{tone})')
    return txr

