import logging as lg
from . Base import Base

class Shades(Base) :
## ====================================================
  def setup(self) :
    super().setup()
    lg.debug('Configuring Shades renderer.')

