#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD.
# See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import numpy as np
import re
from ase.cell import Cell

from nomad.units import ureg
from nomad.parsing.file_parser import BasicParser


class TinkerParser(BasicParser):
    def __init__(self):
        re_f = r'\-*\d+\.\d+E*e*\-*\+*\d*'

        def get_positions(val):
            res = dict(lattice_vectors=[], atom_labels=[], atom_positions=[])
            try:
                cell_par = re.search(rf'({re_f} +{re_f} +{re_f} +{re_f} +{re_f} +{re_f})', val)
                res['lattice_vectors'] = Cell.fromcellpar([float(v) for v in cell_par.group(1).split()]).array * ureg.angstrom
                labels, positions = zip(*re.findall(rf'\d+ +([A-Z][a-z]*) +({re_f} +{re_f} +{re_f} +)\d+', val))
                res['atom_labels'] = labels
                res['atom_positions'] = np.array([v.split() for v in positions], dtype=np.dtype(np.float64)) * ureg.angstrom
            except Exception:
                pass
            return res

        super().__init__(
            specifications=dict(
                name='parsers/tinker', code_name='TINKER', domain='dft',
                mainfile_contents_re=r'TINKER  ---  Software Tools for Molecular Design'),
            units_mapping=dict(energy=ureg.kcal / 6.02214076e+23, length=ureg.angstrom),
            program_version=r'\# +(Version [\d\.]+)',
            auxilliary_files=r'Coordinate File +(\S+)',
            atom_labels_atom_positions_lattice_vectors=(
                rf'\d+ +\w+ +.+\s*({re_f} +{re_f} +{re_f} +{re_f} +{re_f} +{re_f}[\s\S]+?)(?:[\(,]|\Z)',
                get_positions),
            # TODO support for various input, output formats
            energy_total=rf'Total Energy +({re_f}) Kcal\/mole')
