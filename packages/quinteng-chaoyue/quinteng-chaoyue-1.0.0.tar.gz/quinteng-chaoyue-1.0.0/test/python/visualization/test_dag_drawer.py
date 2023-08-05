# This code is part of Quinteng.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests for DAG visualization tool."""

import unittest

from quinteng import QuantumRegister, QuantumCircuit
from quinteng.test import QuintengTestCase
from quinteng.tools.visualization import dag_drawer
from quinteng.visualization.exceptions import VisualizationError
from quinteng.converters import circuit_to_dag


class TestDagDrawer(QuintengTestCase):
    """Quinteng DAG drawer tests."""

    def setUp(self):
        super().setUp()
        qr = QuantumRegister(2, "qr")
        circuit = QuantumCircuit(qr)
        circuit.cx(qr[0], qr[1])
        circuit.cx(qr[0], qr[1])
        self.dag = circuit_to_dag(circuit)

    def test_dag_drawer_invalid_style(self):
        """Test dag draw with invalid style."""
        self.assertRaises(VisualizationError, dag_drawer, self.dag, style="multicolor")


if __name__ == "__main__":
    unittest.main(verbosity=2)
