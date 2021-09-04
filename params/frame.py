import logging as lg


## Exports
## ====================================================

def random_frame() :
  from utils import get_config

  config = get_config()
  return {
    'light'    : random_params(config['light']),
    'camera'   : random_params(config['camera']),
    'geometry' : random_params(config['geometry']),
  }

def frame_dist(f0, f1) :
  camvals = lambda frame : [
    v for k,v in frame['camera'].items()
  ]
  dist = lambda a, b : (
    (a - b) ** 2
  )

  f0, f1 = camvals(f0), camvals(f1)
  d =  sum(dist(a,b) for a, b in zip(f0, f1))

  return d

## Params generator
## ====================================================

def random_params(alist_ranges) :
  from random import random
  r = lambda a, b: (
    a + (b-a) * random()
  )

  params = {
    k: r(*v['range'])
    for (k, v) in alist_ranges.items()
    if type(v) is dict and 'range' in v
  }

  return params
