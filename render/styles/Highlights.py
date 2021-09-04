import logging as lg
from . Base import Base

class Highlights(Base) :
## ====================================================
  def setup(self) :
    super().setup()
    lg.debug('Configuring Highlights renderer.')

