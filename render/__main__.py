## Setup Logging
## ====================================================
import logging as lg
lg.basicConfig(
  level=lg.INFO,
  format='%(levelname)-8s: %(message)s'
)

import bpy, mathutils

from . materials.Materials import Materials
from . materials.Textures import Textures

## Imports
## ====================================================
from . cli_args import cli_args
from . modules_selector import get_modules

from utils import read_ndjson, get_config, Get, Set

## Read CLI args
## ===================================================
args = cli_args()
if args.verbose : lg.getLogger().setLevel(lg.DEBUG)
lg.debug('Args: %s', args)

## Read Config
## ====================================================
config = get_config(
  path=args.config,
  style=args.style
)

Get.config(
  mod_bpy = bpy,
  mod_mathutils = mathutils,
)

Set.runtime('output', args.output)
Set.runtime('debug_scene_before_render',
            args.debug_scene_before_render)

## Select Modules
## ====================================================
Scene, Frame = get_modules(args.style)

## Setup Scene
## ====================================================
scene = Scene(config, args.scene)
scene.setup()

## Setup Materials
## ====================================================
Materials.setup()
Textures.setup()

## Render frames
## ====================================================
for i, frame_data in (
    enumerate(read_ndjson(args.frames))
) :
  
  Frame.render(i, frame_data)
