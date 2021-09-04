import logging as lg

from . FrameDefault import FrameDefault
from ..scene.Render import Render
from utils import Get, Set

class FrameSketchGeom(FrameDefault) :

  @classmethod
  def render(cls, i, data) :
    tag = 'FrameSketchGeom: render'

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
    
