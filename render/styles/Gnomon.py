import logging as lg
from . Base import Base

class Gnomon(Base) :
## ====================================================
  def setup(self) :
    super().setup()
    lg.debug('Configuring Gnomon renderer.')

