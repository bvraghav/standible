import logging as lg

from utils import Get, Set

import bpy
from bpy import (
  context as C,
  data    as D,
  ops     as Op
)

import mathutils as M
import math as m

class UvUnwrap :

  @classmethod
  def do(cls, obj_name) :

    obj = Get.bpy_object(obj_name)

    area, region = [
      (area, region)
      for area in C.screen.areas
      for region in area.regions
      if area.type == 'VIEW_3D'
      if region.type =='WINDOW'
    ][0]

    scene = Get.scene()
    view_layer = Get.view()

    override = C.copy()
    override.update({
      'active_object'               : obj         ,
      'area'                        : area        ,
      'edit_object'                 : obj.data    ,
      'editable_objects'            : [obj]       ,
      'mode'                        : 'EDIT_MESH' ,
      'object'                      : obj         ,
      'objects_in_mode'             : [obj]       ,
      'objects_in_mode_unique_data' : [obj]       ,
      'region'                      : region      ,
      'scene'                       : scene       ,
      'selectable_objects'          : [obj]       ,
      'selected_editable_objects'   : [obj]       ,
      'selected_objects'            : [obj]       ,
      'view_layer'                  : view_layer  ,
      'visible_objects'             : [obj]       ,
    })

    Op.uv.smart_project (override)
    lg.info('smart_uv_unwrap: %s', ' '.join([
      '%s:%s' % (k,v) for (k,v) in ({
        'area'       : area.type       ,
        'region'     : region.type     ,
        'obj'        : obj.name        ,
        'scene'      : scene.name      ,
        'view_layer' : view_layer.name ,
      }).items()
    ]))
  
