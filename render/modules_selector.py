import logging as lg
from importlib import import_module
import sys
from pathlib import Path

## Get Modules
## ====================================================
def get_modules(style) :

  return (
    get_scene(style),
    get_frame(style),
  )

# ## Get materials
# ## ====================================================
# def get_materials(style) :
#   from . materials import Materials
#   return Materials

## Get renderer
## ====================================================
def get_renderer(style) :
  from . styles import (
    Base,
    Contour,
    Gnomon,
    Sketch,
    Highlights,
    Midtones,
    Shades,
    Shadows,
    Diffuse,
  )

  lg.debug('get_renderer: style: %s', style)
  Renderer = {
    'contour'    : Contour, 
    'gnomon'     : Gnomon, 
    'sketch'     : Sketch, 
    'highlights' : Highlights,
    'midtones'   : Midtones, 
    'shades'     : Shades, 
    'shadows'    : Shadows, 
    'diffuse'    : Diffuse, 
  }.get(style, Base)

  return Renderer

## Get scene
## ====================================================

def get_scene(style) :
  from . scene import (
    SceneDefault, SceneGnomon, SceneSketchGeom,
  )

  Scene = {
    'gnomon': SceneGnomon,
    'sketch_geom': SceneSketchGeom,
    'sketch_geom_no_free': SceneSketchGeom,
  }.get(style, SceneDefault)

  return Scene

## Get frames
## ====================================================

def get_frame(style) :
  from . frame import (
    FrameDefault, FrameGnomon, FrameSketchGeom,
  )

  Frame = {
    'gnomon': FrameGnomon,
    'sketch_geom': FrameSketchGeom,
  }.get(style, FrameDefault)

  return Frame
