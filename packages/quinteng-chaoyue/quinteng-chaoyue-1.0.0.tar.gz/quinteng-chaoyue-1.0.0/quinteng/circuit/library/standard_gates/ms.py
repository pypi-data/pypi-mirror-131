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

"""Global Mølmer–Sørensen gate."""

from typing import Optional
import warnings
from quinteng.circuit.gate import Gate
from quinteng.circuit.quantumregister import QuantumRegister
from quinteng.circuit.parameterexpression import ParameterValueType


class MSGate(Gate):
    """MSGate has been deprecated.
    Please use ``GMS`` in ``quinteng.circuit.generalized_gates`` instead.

    Global Mølmer–Sørensen gate.

    The Mølmer–Sørensen gate is native to ion-trap systems. The global MS can be
    applied to multiple ions to entangle multiple qubits simultaneously.

    In the two-qubit case, this is equivalent to an XX(theta) interaction,
    and is thus reduced to the RXXGate.
    """

    def __init__(self, num_qubits: int, theta: ParameterValueType, label: Optional[str] = None):
        """Create new MS gate."""
        warnings.warn(
            "The quinteng.circuit.library.standard_gates.ms import "
            "is deprecated as of 0.16.0. You should import MSGate "
            "using quinteng.circuit.library.generalized_gates "
            "instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__("ms", num_qubits, [theta], label=label)

    def _define(self):
        # pylint: disable=cyclic-import
        from quinteng.circuit.quantumcircuit import QuantumCircuit
        from .rxx import RXXGate

        theta = self.params[0]
        q = QuantumRegister(self.num_qubits, "q")
        qc = QuantumCircuit(q, name=self.name)
        for i in range(self.num_qubits):
            for j in range(i + 1, self.num_qubits):
                qc._append(RXXGate(theta), [q[i], q[j]], [])

        self.definition = qc
