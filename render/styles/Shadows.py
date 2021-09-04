import logging as lg
from . Base import Base

class Shadows(Base) :
## ====================================================
  def setup(self) :
    super().setup()
    lg.debug('Configuring Shadows renderer.')

