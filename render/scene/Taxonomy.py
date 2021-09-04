import logging as lg

from utils import Get

import bpy
from bpy import (
  context as C,
  data as D,
  ops as Op,
)
import mathutils as M
import math as m

class Taxonomy :
## ====================================================

  def setup(self) :

    self.create_scene_may_be()
    self.scene_remove_others()
    self.create_world_may_be()
    self.create_view_may_be()
    self.create_collections_may_be()
    

  ## Basic try catch wrapper for create
  ## --------------------------------------------------
  def create_xxx_may_be(
      self, key_exists, key_create, key,
      Error = LookupError,
  ) :
    def try_construct(*args, **kwargs) :
      try :
        if not key_exists(*args, **kwargs) :
          raise LookupError(
            f'{key} not found in Blender DB'
          )

      except Error as e :
        name = Get.fmt(key, **kwargs)
        tag = f'Taxonomy: create_{key}_may_be'
        lg.info(f'{tag}: name:{name}')
        key_create(*args, **kwargs)

        lg.info(f'{tag}: ...done')

    return try_construct

  def __getattr__(cls, attr) :
    lg.debug(f'Taxonomy: __getattr__: attr: {attr}')

    fixed = 'create_may_be'.split('_')
    attr = attr.split('_')
    
    if [*attr[:1], *attr[-2:]] == fixed :
      from functools import partial

      key = '_'.join(attr[1:-2])

      key_exists = (
        getattr(cls, f'{key}_exists', False)
        or getattr(cls, f'{key}_exist')
      )

      key_create = getattr(cls, f'{key}_create')
      
      # return partial(
      #   cls.check_xxx_may_be,
      #   key_exists,
      #   key_create,
      #   key        
      # )

      return cls.create_xxx_may_be(
        key_exists, key_create, key
      )

    raise AttributeError(
      f'Taxonomy.{attr} does not exist.'
    )

  ## Scene
  ## --------------------------------------------------
  def scene_exists(self) :
    return Get.scene()

  def scene_create(self) :
    scene = D.scenes.new(Get.fmt('scene'))
    lg.info(f'Taxonomy: scene_create: {scene.name}')

    return scene

  def scene_remove_others(self) :
    scene = Get.scene()

    keys = []
    for scn in D.scenes.values() :
      if scn is not scene :
        keys.append(scn.name)
        D.scenes.remove(scn)

    lg.info(
      f'Taxonomy: scene_remove_others: {keys}'
    )
  
  ## World
  ## --------------------------------------------------
  def world_exists(self) :
    scene = Get.scene()
    world = Get.world()
    return world and world == scene.world

  def world_create(self) :
    scene = Get.scene()
    scene.world = (
      Get.world()
      or D.worlds.new(Get.fmt('world'))
    )
    lg.info(
      'Taxonomy: world_create: {scene.world.name}'
    )

    return scene.world

  ## Collection
  ## --------------------------------------------------
  def collection_exists(self, name) :
    collection = Get.collection(name)
    scene_collections = (
      Get.scene().collection.children.keys()
    )
    return (
      collection
      and
      collection.name in scene_collections
    )

  def collection_create(self, name) :
    scene = Get.scene()
    name = Get.fmt(
      'collection',
      name = Get.config(
        f'collections/{name}/name'
      ),
    )

    collection = D.collections.new(name)
    scene.collection.children.link(collection)

    lg.info(
      f'Taxonomy: collection_create: {collection.name}'
    )

    return collection

  ## Collections
  ## --------------------------------------------------
  def collections_exist(self) :
    style = Get.config('runtime/style')

    collections = Get.config(
      f'views/{style}/collections'
    )

    return all(
      Get.collection(name)
      for name in collections
    )

  def collections_create(self) :
    tag = 'Taxonomy: collections_create'

    style = Get.config('runtime/style')

    collections = Get.config(
      f'views/{style}/collections'
    )

    view_collections = (
      Get.view(style)
      .layer_collection
      .children
    )

    visible_collection = Get.fmt_collection()
    lg.info('{}: visible collection: {}'.format(
      tag, visible_collection
    ))

    for name in collections :
      self.create_collection_may_be(name)

      collection_name = Get.fmt_collection(name)
      view_collections[collection_name].exclude = (
        visible_collection != collection_name
      )    

    lg.info('{}: {} ...done'.format(
      tag, 
      [cl.name for cl in Get.collections(style)],
    ))

  ## View Layer
  ## --------------------------------------------------
  def view_exists(self, name=None) :
    name = name or Get.config('runtime/style')
    return Get.view(name)

  def view_create(self, name=None) :
    name = name or Get.config('runtime/style')
    name = Get.fmt(
      'view',
      name=Get.config(
        f'views/{name}/name'
      )
    )

    view = Get.scene().view_layers.new(name)

    lg.info(f'Taxonomy: view_create: {view.name}')

    return view
  
    
