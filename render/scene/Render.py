import logging as lg
from abc import abstractmethod

from utils import Get, Set

import bpy
from bpy import (
  context as C,
  data as D,
  ops as Op
)

import math as m
import mathutils as M

class Render() :
## ====================================================
  @classmethod
  def setup(cls) :
    tag = f'Render: setup'
    lg.debug(f'{tag}: Configuring Base renderer.',)

    scene = Get.scene()

    lg.info(f'{tag}: Setting up scene.render')
    Set.attributes_from_config(
      scene.render,
      Get.config('renderer/render')
    )

    lg.info(f'{tag}: Setting up scene.eevee')
    Set.attributes_from_config(
      scene.eevee,
      Get.config('renderer/eevee')
    )

    lg.info(f'{tag}: Setting up scene.world')
    Set.attributes_from_config(
      scene.world,
      Get.config('renderer/world')
    )

    if Get.collection('freestyle') :
      cls.lineset_setup()
      cls.linestyle_setup()

    # cls.compositor_setup()

  @classmethod
  def render(cls, outpath) :
    lg.debug('Render: Rendering to %s.', outpath)
    scene = Get.scene()

    view = Get.view()

    scene.render.filepath = str(outpath)
    # scene.camera = Get.camera()

    if Get.runtime('debug_scene_before_render') :
      raise Exception()

    Op.render.render(
      write_still = True,
      layer = view.name,
      scene = scene.name
    )
    
  @classmethod
  def lineset_setup(cls) :
    tag = 'Render: lineset_setup'

    style = Get.config('runtime/style')
    name = Get.fmt(
      'lineset',
      name=Get.fmt_lineset(style)
    )
    lineset = (
      Get.view(style)
      .freestyle_settings
      .linesets
      .new(name)
    )
    lg.info(f'{tag}: name: {lineset.name}')

    lineset.collection = Get.collection('freestyle')
    lg.info(
      f'{tag}: lineset.collection: '
      f'{lineset.collection.name}'
    )

    lg.info(f'{tag}: Setting up lineset')
    Set.attributes_from_config(
      lineset,
      Get.config('freestyle/lineset')
    )

  @classmethod
  def linestyle_setup(cls) :
    tag = '{}: linestyle_setup'.format(
      cls.__name__
    )

    ## Freestyle linestyle
    ## --------------------------------------------------
    linestyle = Get.linestyle()

    if not linestyle :
      name = Get.fmt('linestyle')
      linestyle = D.linestyles.new(name)

    Get.lineset().linestyle = linestyle
    lg.info(f'{tag}: Setting up linestyle: '
            f'{linestyle.name}')

    Set.attributes_from_config(
      linestyle,
      Get.config('freestyle/linestyle')
    )
    # Add modifiers from config
    for mod_config in (
        Get.config('freestyle/linestyle_modifiers')
        .values()
    ) :
      mod_type       = mod_config['type']
      mod_name       = mod_config['name']
      mod_modifiers  = mod_config['modifiers']
      mod_attributes = mod_config['attributes']

      lymods = getattr(linestyle, mod_modifiers)
      mod = lymods.new(mod_name, mod_type)
      lg.info(f'{tag}: add {mod_modifiers}: {mod.name}')

      lg.info(f'{tag}: Setting up {mod.name}')
      Set.attributes_from_config(
        mod,
        mod_attributes
      )

  @classmethod
  def compositor_setup(cls) :
    tag = 'Render: compositor_setup'
    lg.info(tag)

    C.scene.use_nodes = True

    nt = C.scene.node_tree
    relay = nt.nodes['Render Layers']
    ct = nt.nodes['Composite']

    ng = nt.nodes.new('CompositorNodeGroup')
    ng.node_tree = D.node_groups['Compose']

    nt.links.new(ng.inputs['Image'], relay.outputs['Image'])
    # nt.links.new(ng.inputs[1], relay.outputs['Alpha'])
    nt.links.new(ct.inputs['Image'], ng.outputs['Image'])

    ct.use_alpha = True

    lg.info(f'{tag}: ...done')

