## Enable logging
## --------------------------------------------------
import logging as lg

lg.basicConfig(
  level=lg.INFO,
  format='%(levelname)-8s: %(message)s'
)

## Import local functions
## ====================================================
from . cli_args import cli_args
from utils      import get_config

## Main
## ====================================================

# Parse cli arguments
args = cli_args()
if args.verbose : lg.getLogger().setLevel(lg.DEBUG)
lg.debug('Args: %s', args)

# config setup
get_config(
  path=args.config,
)

if args.command == 'create-frames' :
  from . create_frames import create_frames
  create_frames(args)

elif args.command == 'create-scene' :
  from . create_scene import create_scene
  create_scene(args)
