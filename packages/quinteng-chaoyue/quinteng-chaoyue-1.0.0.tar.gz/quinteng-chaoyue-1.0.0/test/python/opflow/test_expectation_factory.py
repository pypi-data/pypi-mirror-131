# This code is part of Quinteng.
#
# (C) Copyright IBM 2018, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test the expectation factory."""

import unittest
from test.python.opflow import QuintengOpflowTestCase

from quinteng.opflow import PauliExpectation, AerPauliExpectation, ExpectationFactory, Z, I, X
from quinteng.utils import has_aer


if has_aer():
    from quinteng import Aer


class TestExpectationFactory(QuintengOpflowTestCase):
    """Tests for the expectation factory."""

    @unittest.skipUnless(has_aer(), "quinteng-aer doesn't appear to be installed.")
    def test_aer_simulator_pauli_sum(self):
        """Test expectation selection with Aer's qasm_simulator."""
        backend = Aer.get_backend("aer_simulator")
        op = 0.2 * (X ^ X) + 0.1 * (Z ^ I)

        with self.subTest("Defaults"):
            expectation = ExpectationFactory.build(op, backend, include_custom=False)
            self.assertIsInstance(expectation, PauliExpectation)

        with self.subTest("Include custom"):
            expectation = ExpectationFactory.build(op, backend, include_custom=True)
            self.assertIsInstance(expectation, AerPauliExpectation)
