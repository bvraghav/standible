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
    prog=' '.join(argv_pre_pruned()),
  )

  ## Optional arguments
  ## --------------------------------------------------

  parser.add_argument(
    '-v', '--verbose', help='Enable log verbosity.',
    action='store_true',
  )

  parser.add_argument(
    '-r', '--style', help='Render style',
    required=True,
  )

  parser.add_argument(
    '-s', '--scene', help='Scene data as ndjson',
    type=Path, metavar='PATH', required=True
  )

  parser.add_argument(
    '-f', '--frames', help='Frames data as ndjson',
    type=Path, metavar='PATH', required=True
  )

  parser.add_argument(
    '-o', '--output', help='Output path.',
    type=Path, metavar='PATH', required=True,
  )

  parser.add_argument(
    '-C', '--config', help='Path to JSON Config file',
    type=Path, metavar='PATH'
  )

  parser.add_argument(
    '--debug-scene-before-render', action='store_true',
    help='Stop execution using a naive exception'
    'just before render. Helps debugging scene.'
  )

  ## Parse CLI
  ## ==================================================
  return parser.parse_args(argv_pruned())

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
