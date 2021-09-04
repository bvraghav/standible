import logging as lg
from . Base import Base

class Diffuse(Base) :
## ====================================================
  def setup(self) :
    super().setup()
    lg.debug('Configuring Diffuse renderer.')

