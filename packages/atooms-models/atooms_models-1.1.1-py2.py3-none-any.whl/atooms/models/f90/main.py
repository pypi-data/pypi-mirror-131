import f2py_jit
from f2py_jit.finline import inline_source

def _merge_source(*sources):
    """Merges `sources` into a unique source."""
    import os
    merged_src = ''
    for source in sources:
        # Check path existence
        source_path = source  # _normalize_path(source)
        with open(source_path) as fh:
            src = fh.read()
        # Merge sources into a single one
        merged_src += src
    return merged_src


source = _merge_source('helpers_3d.f90', 'inverse_power.f90', 'cut_shift.f90', 'interaction.f90')
source = inline_source(source, ignore='tailor,forces,compute,smooth,compute_vector,smooth_vector')
uid = f2py_jit.build_module(source, extra_args='--opt="-O3 -ffree-form -ffree-line-length-none"')
interaction = f2py_jit.import_module(uid)
interaction.potential.setup(sigma=[[1.0]], epsilon=[[1.0]], exponent=12)
interaction.cutoff.setup(rcut=[[2.5]])

import numpy
from atooms.core.utils import Timer
from atooms.trajectory import Trajectory
t = Trajectory('/home/coslo/usr/atooms/data/lj_N1000_rho1.0.xyz')
s = t[0]
s.species_layout = 'F'
pos = s.dump('pos', order='F')
box = s.dump('box')
ids = s.dump('spe', dtype='int32')
forces = numpy.empty_like(pos)
with Timer():
    for _ in range(100):
        epot, virial = interaction.interaction_vector.forces(box, pos, ids, forces)
    print(epot)

with Timer():
    for _ in range(100):
        epot, virial = interaction.interaction.forces(box, pos, ids, forces)
    print(epot)
