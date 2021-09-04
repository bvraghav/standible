import logging as lg
from pathlib import Path

def create_scene(args) :
  from utils import get_config
  from utils import write_data
  import random

  config = get_config()
  lg.info(f'create_scene: config (keys): {list(config.keys())}')

  textures = get_textures(config)
  lg.info(f'create_scene: textures: {textures}')

  solids = get_solids(config) or get_meshes(config)
  lg.info(f'create_scene: solids(len): {len(solids)}')

  r = lambda: random.random()
  r3 = lambda: [r(), r(), r()]
  scene = {
    'geometry' : {
      'name'   : random.choice(solids),
    },
    'texture'  : {
      'name'   : random.choice(textures),
      'origins' : {
        k: r3() for k in
        config['textures']['image_mapping']
      }
    },
  }

  write_data([scene], args.output)

def get_textures(config) :
  return get_keys_or_filter_dir(
    config, 'textures',
    predicate = lambda x: (
      Path(x).is_dir()
    ),
  )

def get_solids(config) :
  return get_keys_or_filter_dir(
    config, 'geometry',
    predicate = lambda x: (
      Path(x).suffix == '.stl'
    ),
  )

def get_meshes(config) :
  return get_keys_or_filter_dir(
    config, 'geometry',
    predicate = lambda x: (
      Path(x).suffix == '.obj'
    ),
  )

def get_keys_or_filter_dir(
    data, key,
    predicate = lambda x: true,
    alist_key = 'name_folder_alist',
    prefix_key = 'prefix',
) :

  if (alist_key in data[key]
      and
      dict is type(data[key][alist_key])) :

    return list(
      data[key][alist_key].keys()
    )

  prefix = data[key][prefix_key]
  lg.debug(f'get_keys_or_filter_dir: prefix: {prefix}')
  lg.debug(f'get_keys_or_filter_dir: globs(len): {len(list(Path(prefix).glob("*")))}')
  return [
    str(fname.name)
    for fname in Path(prefix).glob('*')
    if predicate(fname)
  ]
  
