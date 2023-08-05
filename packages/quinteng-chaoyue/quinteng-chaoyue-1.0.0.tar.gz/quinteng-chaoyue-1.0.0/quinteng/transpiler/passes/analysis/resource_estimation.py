# This code is part of Quinteng.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Automatically require analysis passes for resource estimation."""

from quinteng.transpiler.basepasses import AnalysisPass
from quinteng.transpiler.passes.analysis.depth import Depth
from quinteng.transpiler.passes.analysis.width import Width
from quinteng.transpiler.passes.analysis.size import Size
from quinteng.transpiler.passes.analysis.count_ops import CountOps
from quinteng.transpiler.passes.analysis.num_tensor_factors import NumTensorFactors
from quinteng.transpiler.passes.analysis.num_qubits import NumQubits


class ResourceEstimation(AnalysisPass):
    """Automatically require analysis passes for resource estimation.

    An analysis pass for automatically running:
    * Depth()
    * Width()
    * Size()
    * CountOps()
    * NumTensorFactors()
    """

    def __init__(self):
        super().__init__()
        self.requires += [Depth(), Width(), Size(), CountOps(), NumTensorFactors(), NumQubits()]

    def run(self, _):
        """Run the ResourceEstimation pass on `dag`."""
        pass
