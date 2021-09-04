import logging as lg
from argparse import Namespace

## Namespace wrappers
## ====================================================

def namespaced(dict_instance) :
  return Namespace(**dict_instance)

def ns(**args) :
  return namespaced(**args)

def hex_to_color(hex) :
  try :
    n = len(hex) // 2           # 3 for RRGGBB and 4
                                # for RRGGBBAA
    hex = int(hex.strip('#'), 16)
    
    rgb = list(map(
      lambda x: ((hex >> (8*x)) & 0xff) / 255.,
      reversed(range(n))
    ))

  except Exception as e :
    raise ValueError(str(e))

  try :
    from mathutils import Color as color
  except ImportError as e :
    lg.warning('hex_to_color: %s', str(e))
    lg.info('Using tuple instead.')
    color = tuple

  return color(rgb)

def color_to_hex(color) :
  return '#{:x}'.format(
    sum(
      int(round(x*255)) << (8*i)
      for (i, x) in
      enumerate(reversed(tuple(color)))
    )
  )
