import logging as lg

from utils import Get, Set

from . SceneDefault import SceneDefault

from . Taxonomy import Taxonomy
from . CameraGnomon import CameraGnomon
from . Light import Light
from . Gnomon import Gnomon
from . Render import Render

class SceneGnomon(SceneDefault) :
  def setup(self) :
    lg.debug(
      'Setting up scene from data: %s',
      Get.config('runtime/scene')
    )

    self.clear_scene()

    Taxonomy().setup()
    CameraGnomon.setup()
    Light.setup()
    Gnomon.setup()
    Render.setup()
