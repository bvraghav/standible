import logging as lg

from utils import Get, Set

from . Mask import Mask

class HatchMask :
  @classmethod
  def setup(cls, mat_name) :
    tag = 'HatchMask: setup'

    group_name = Get.config(
      f'textures/image_mapping/{mat_name}/node'
    )

    # Duplicate material
    mat = Mask.dup_mat('hatch', mat_name)

    # Holistic
    nt = mat.node_tree
    out_nd = nt.nodes['Material Output']
    gr_nd = nt.nodes[group_name]
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
