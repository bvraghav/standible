import logging as lg
from . Base import Base

class Sketch(Base) :
## ====================================================
  def setup(self) :
    super().setup()
    lg.debug('Configuring Sketch renderer.')

