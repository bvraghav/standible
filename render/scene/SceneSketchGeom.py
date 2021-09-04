import logging as lg

from utils import Get, Set

from . SceneDefault import SceneDefault

from . Taxonomy import Taxonomy
from . Camera import Camera
from . Light import Light
from . Gnomon import Gnomon
# from . Plane import Plane
from . Payload import Payload
from . Render import Render

class SceneSketchGeom(SceneDefault) :

  def setup(self) :
    lg.debug(
      'Setting up scene from data: %s',
      Get.config('runtime/scene')
    )

    self.clear_scene()

    Taxonomy().setup()
    Camera.setup()
    Light.setup()
    # Plane.setup()
    Payload.setup()
    Render.setup()
