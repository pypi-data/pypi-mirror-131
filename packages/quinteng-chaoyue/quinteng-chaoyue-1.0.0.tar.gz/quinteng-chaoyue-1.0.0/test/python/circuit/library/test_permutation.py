# This code is part of Quinteng.
#
# (C) Copyright IBM 2017, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test library of permutation logic quantum circuits."""

import unittest
import numpy as np
from ddt import ddt, data

from quinteng.test.base import QuintengTestCase
from quinteng.circuit import QuantumCircuit
from quinteng.circuit.exceptions import CircuitError
from quinteng.circuit.library import Permutation
from quinteng.circuit.library.generalized_gates.permutation import _get_ordered_swap
from quinteng.quantum_info import Operator


@ddt
class TestPermutationLibrary(QuintengTestCase):
    """Test library of permutation logic quantum circuits."""

    def test_permutation(self):
        """Test permutation circuit."""
        circuit = Permutation(num_qubits=4, pattern=[1, 0, 3, 2])
        expected = QuantumCircuit(4)
        expected.swap(0, 1)
        expected.swap(2, 3)
        expected = Operator(expected)
        simulated = Operator(circuit)
        self.assertTrue(expected.equiv(simulated))

    def test_permutation_bad(self):
        """Test that [0,..,n-1] permutation is required (no -1 for last element)."""
        self.assertRaises(CircuitError, Permutation, 4, [1, 0, -1, 2])

    @data(4, 5, 10, 20)
    def test_get_ordered_swap(self, width):
        """Test get_ordered_swap function produces correct swap list."""
        np.random.seed(1)
        for _ in range(5):
            permutation = np.random.permutation(width)
            swap_list = _get_ordered_swap(permutation)
            output = list(range(width))
            for i, j in swap_list:
                output[i], output[j] = output[j], output[i]
            self.assertTrue(np.array_equal(permutation, output))
            self.assertLess(len(swap_list), width)


if __name__ == "__main__":
    unittest.main()
