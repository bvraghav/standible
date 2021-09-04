import logging as lg

## Exports
## ====================================================
__all__ = [
  'get_config',
  'set_runtime'
]

## Cache
## ====================================================
from argparse import Namespace

cache = Namespace()
env_config = 'STANDIBLE_CONFIG'

## Config
## ====================================================

def read_config(config) :
  from . io import read_json

  lg.info('read_config: Reading file: %s', config)
  return read_json(config)

def get_config(
    key=None, path=None, use_cache=True,
    **kwargs
) :
  from os import getenv
  from pathlib import Path

  assert(use_cache or path)
  global cache

  if (
      path                       # Simply invalidate
                                 # cache if path
                                 # argument is passed
      or not (                   # OR
        hasattr(cache, 'config') # Populate cache if 
        and                      # queried for the 
        cache.config             # first time.
      )                          # 
  ) :
    path = (
      path
      or getenv(env_config)
      or 'config.json'
    )
    path = Path(path).expanduser().resolve()

    kwargs.update({
      'configpath': str(path)
    })
    config = read_config(path)

    if use_cache:
      cache.config = config

  else :
    config = cache.config

  if kwargs :
    lg.debug(f'get_config: updating runtime: {kwargs}')
    set_runtime(**kwargs)
    config.update(cache.config)

  return config.get(key, config)


def set_runtime(**kwargs) :
  if not hasattr(cache, 'config') :
    cache.config = {}

  if 'runtime' not in cache.config :
    cache.config['runtime'] = {}

  cache.config['runtime'].update(kwargs)
