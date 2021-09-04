import logging as lg

from utils import Get, Set

# from . HatchMask import HatchMask
# from . ShadowMask import ShadowMask

class Mask :
  # @classmethod
  # def setup(cls, mat_name) :
  #   chooser = {
  #     'highl': HatchMask,
  #     'midto': HatchMask,
  #     'shade': HatchMask,
  #     'shama': ShadowMask,
  #   }

  #   MaskManager = chooser(mat_name)
  #   MaskManager.setup()

  @classmethod
  def setup(cls, mat_name) :
    tag = 'Mask: setup'

    key_prefix = f'materials/{mat_name}'
    src_mat = f'{key_prefix}/src/material'
    src_grp = f'{key_prefix}/src/node_group'
    tgt_nod = f'{key_prefix}/target/node'

    lg.info(
      f'{tag}: mat:{mat_name}, src:{src_mat}'
      f'src.grp:{src_grp} tgt.nod:{tgt_nod}'
    )

    src_mat = Get.config(src_mat)
    src_grp = Get.config(src_grp)
    tgt_nod = Get.config(tgt_nod)

    # Duplicate material
    mat = Mask.dup_mat(src_mat, mat_name)

    # Holistic
    nt = mat.node_tree
    out_nd = nt.nodes[tgt_nod]
    gr_nd = nt.nodes[src_grp]
    nt.links.new(out_nd.inputs[0], gr_nd.outputs[0])

    # Duplicate node group
    gr_name = gr_nd.node_tree.name
    gr_nt = gr_nd.node_tree.copy()
    gr_nt.name = '%s-%s' % (mat_name, gr_name)
    gr_nd.node_tree = gr_nt
    lg.info(f'{tag}: {gr_name} -> {gr_nt.name}')

    # Detail
    out_nd = gr_nt.nodes['Group Output']
    inv_nd = gr_nt.nodes['Invert']
    gr_nt.links.new(out_nd.inputs[0], inv_nd.outputs[0]) 

    mat = Get.mat(mat_name)
    lg.info(f'{tag}: {mat.name} ...done')

  @classmethod
  def dup_mat(
      cls,
      src_name,
      dst_name,
      fake_user=True
  ) :
    mat_orig = Get.mat(src_name)
    mat = mat_orig.copy()
    mat.name = Get.fmt_mat(dst_name)
    mat.use_fake_user = bool(fake_user)

    lg.debug('dup_mat: %s -> %s (Fake:%s) ...done',
             src_name, dst_name, fake_user)

    return mat
