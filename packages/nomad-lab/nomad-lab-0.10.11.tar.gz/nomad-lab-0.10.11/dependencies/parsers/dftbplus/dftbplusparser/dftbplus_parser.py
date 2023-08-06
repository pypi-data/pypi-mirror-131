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

from nomad.units import ureg
from nomad.parsing.file_parser import BasicParser


class DFTBPlusParser(BasicParser):
    def __init__(self):
        super().__init__(
            specifications=dict(
                name='parsers/dftbplus', code_name='DFTB+', domain='dft',
                mainfile_contents_re=r'^ Fermi distribution function\s*',
                mainfile_mime_re=r'text/.*'),
            units_mapping=dict(length=ureg.bohr, energy=ureg.hartree),
            atom_positions=r'Coordinates of moved atoms \(au\)\:\s*([\s\S]+?)\n *\n',
            energy_reference_fermi=(r'Fermi energy\:\s*(\S+)', lambda x: [x]),
            energy_total=r'Total energy\:\s*(\S+)',
            energy_free=r'Total Mermin free energy\:\s*(\S+)',
            atom_forces=r'Total Forces\s*([\s\S]+?)\n *\n')
