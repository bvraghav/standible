import logging as lg
from . Base import Base

class Midtones(Base) :
## ====================================================
  def setup(self) :
    super().setup()
    lg.debug('Configuring Midtones renderer.')

