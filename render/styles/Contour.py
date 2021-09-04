import logging as lg
from . Base import Base

class Contour(Base) :
## ====================================================
  def setup(self) :
    super().setup()
    lg.debug('Configuring Contour renderer.')

