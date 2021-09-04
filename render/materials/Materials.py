import logging as lg

from utils import Get, Set

class Materials :
  @classmethod
  def setup(cls) :
    tag = 'Materials: setup'

    style = Get.config('runtime/style')

    materials = (
      Get.config(f'collections/{style}/materials')
    )
    for obj, mat in materials.items() :
      from . UvUnwrap import UvUnwrap

      cls.mat_setup(mat)
      cls.mat_assign(mat, obj)
      UvUnwrap.do(obj)

  @classmethod
  def mat_setup(cls, mat_name) :
    tag = 'Materials: mat_setup'

    lg.info(f'{tag}: mat_name: {mat_name}')

    try :
      mat = Get.mat(mat_name)
      if not mat: raise LookupError(
          f'{tag}: Mat `{mat_name}\' not found.'
      )

    except LookupError as e :
      lg.warning(str(e))

      mat = cls.mat_create(mat_name)
      if not mat : raise

    mat.use_fake_user = True
    lg.info(f'{tag}: mat: {mat.name} '
            f'fake: {mat.use_fake_user}')

    return mat

  @classmethod
  def mat_assign(cls, mat_name, obj_name) :
    tag = 'Materials: mat_assign'

    lg.info(f'{tag}: {mat_name} -> {obj_name}')

    mat = Get.mat(mat_name)
    obj = Get.bpy_object(obj_name)

    if not obj.data.materials :
      obj.data.materials.append(mat)

    slot = obj.material_slots[0]
    slot.link = 'OBJECT'
    slot.material = mat

    lg.info(
      f'{tag}: obj:{obj.name} mat:{mat.name}'
    )

  @classmethod
  def mat_create(cls, name) :
    tag = 'Materials: mat_create'

    mat_type = Get.config(
      f'materials/{name}/type'
    )
    
    lg.info(f'{tag}: {name} {mat_type}')

    if mat_type == 'mask' :
      from . Mask import Mask

      Mask.setup(name)
      mat = Get.mat(name)

      return mat
