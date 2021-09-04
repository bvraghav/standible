## CLI Args
## ====================================================

def cli_args() :
  import argparse
  from pathlib import Path

  parser = argparse.ArgumentParser(
    description="Generate parameters to create a 3D "
    "scene.",
    formatter_class=(
      argparse.ArgumentDefaultsHelpFormatter
    ),
    # prog=' '.join(argv_pre_pruned()),
  )

  ## Sub-Parsers
  ## --------------------------------------------------
  parser_master = parser
  subparsers = parser.add_subparsers(dest='command')

  ## Optional arguments
  ## --------------------------------------------------

  parser.add_argument(
    '-v', '--verbose', help='Enable log verbosity.',
    action='store_true',
  )

  parser.add_argument(
    '-C', '--config', help='Path to JSON Config file',
    type=Path, metavar='PATH'
  )

  parser.add_argument(
    '-o', '--output', help='Output path.',
    type=Path, metavar='PATH', default='-',
  )

  ## Create Frame Subparser
  ## ====================================================
  parser = subparsers.add_parser('create-frames')

  ## positional arguments
  ## --------------------------------------------------

  parser.add_argument(
    'n_frames', help='Total number of frames',
    type=int,
  )

  parser.add_argument(
    'n_keyframes', help='Number of keyframes',
    type=int,
  )

  ## Create Scene Subparser
  ## ==================================================
  parser = subparsers.add_parser('create-scene')

  ## Parse CLI
  ## ==================================================
  parser = parser_master
  return parser.parse_args()

def argv_pre_pruned() :
  import sys
  argv = sys.argv

  n = (
    0 if '--' not in argv
    else argv.index('--')
  )
  return argv[:1+n]

def argv_pruned() :
  import sys
  argv = sys.argv

  if '--' not in argv :
    argv = []
  else :
    argv = argv[argv.index('--') + 1:]

  return argv
