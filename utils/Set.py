import logging as lg
from utils import set_runtime

class Set :
  @classmethod
  def runtime(cls, *args, **kwargs) :
    if len(args) == 2 :
      k, v = args
      kwargs.update({k: v})

    set_runtime(**kwargs)

  @classmethod
  def attributes_from_config (
      cls, bpy_object, config, excludes=[]
  ):
    for attr in config :
      if (
          (
            not excludes
            or 
            attr not in excludes
          )

          and

          hasattr(bpy_object, attr)
      ) :
        val = config[attr]
        lg.debug(
          'utils.Set: attributes_from_config: '
          f'{attr} <- {val}'
        )
        setattr(bpy_object, attr, val)
