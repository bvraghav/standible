import logging as lg

from ..scene.Render import Render
from utils import Get, Set

import bpy
from bpy import (
  context as C,
  data    as D,
  ops     as Op
)

import mathutils as M
import math as m

class FrameDefault :
## ====================================================

  @classmethod
  def render(cls, i, data) :
    tag = 'FrameDefault: render'

    Set.runtime('frame', data)
    lg.info('{}: runtime/frame/data: {}'.format(
      tag, Get.runtime('frame')
    ))

    cls.set_light()
    cls.set_camera()
    cls.set_payload()

    out = Get.output(
      prefix=Get.config('runtime/output'),
      index=i
    )
    Render.render(out)

  @classmethod
  def set_light(cls) :
    tag = 'FrameDefault: set_light'

    light_data = Get.runtime('frame/light')
    pos_keys = [
      'distance', 'altitude', 'azimuth'
    ]
    pos_data = {
      k:light_data[k] for k in pos_keys
    }
    pos = cls.sph_to_cart(**pos_data)

    target = M.Vector(
      Get.config('light/target')
    )
    ort = cls.orient(pos, target)

    ## Light setup
    ## --------------------------------------------------
    light = Get.light()
    light.matrix_world.translation = M.Vector(pos)
    light.rotation_euler = M.Euler(ort)
    ## --------------------------------------------------

    lg.info(f'{tag}: Light: pos: {pos}')
    lg.info(f'{tag}: Light: ort: {ort}')

  @classmethod
  def set_camera(cls) :

    camera_data = Get.runtime('frame/camera')
    pos_keys = [
      'distance', 'altitude', 'azimuth'
    ]
    pos_data = {
      k:camera_data[k] for k in pos_keys
    }
    pos = cls.sph_to_cart(**pos_data)

    target = M.Vector(
      Get.config('camera/target')
    )
    ort = cls.orient(pos, target)

    ## Camera Setup
    ## --------------------------------------------------
    camera = Get.camera()
    camera.matrix_world.translation = M.Vector(pos)
    camera.rotation_euler = M.Euler(ort)
    cam = camera.data
    cam.shift_x = camera_data['shift_x']
    cam.shift_y = camera_data['shift_y']
    ## --------------------------------------------------

  @classmethod
  def set_payload(cls) :

    camera_data = Get.runtime('frame/geometry')

    z_rot = camera_data['rotation']
    ort = M.Euler([0, 0, z_rot])

    ## Payload Setup
    ## --------------------------------------------------
    payload = Get.payload()
    payload.rotation_euler = ort

    ## Legacy code (for reference)
    ## TODO: delete it.
    ##-----------------------------------
    # cls.rotate_mesh(
    #   payload.data,
    #   M.Euler(ort),
    # )
    ## --------------------------------------------------

  @classmethod
  def sph_to_cart(
      cls,
      distance,
      altitude,
      azimuth,
      degrees = False,
      geographic = False
  ) :
    r = distance
    theta = altitude
    phi = azimuth

    if degrees :
      r, theta, phi = (
        m.radians(r),
        m.radians(theta),
        m.radians(phi),
      )

    if geographic :
      theta = 0.5*m.pi - theta

    x = r * m.sin(theta) * m.cos(phi)
    y = r * m.sin(theta) * m.sin(phi)
    z = r * m.cos(theta)

    return [x, y, z]

  @classmethod
  def orient(cls, pos, tgt) :
    pos = M.Vector(pos)
    tgt = M.Vector(tgt)
    return list(
      (tgt-pos).to_track_quat('-Z', 'Y').to_euler()
    )

  @classmethod
  def rotate_mesh(cls, bpy_mesh, euler) :
    '''TODO: DELETE
Legacy code for mesh rotation.'''
    import bmesh

    bm = bmesh.new()
    bm.from_mesh(bpy_mesh)

    bmesh.ops.rotate(
      bm,
      cent   = M.Vector((0,0,0)),
      matrix = euler.to_matrix().to_4x4(),
      verts  = bm.verts,
    )

    bm.to_mesh(bpy_mesh)
    bm.free()

    
