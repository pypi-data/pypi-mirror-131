# This code is part of Quinteng.
#
# (C) Copyright IBM 2021
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests for quinteng/version.py"""

from quinteng import __quinteng_version__
from quinteng import __version__
from quinteng.test import QuintengTestCase


class TestVersion(QuintengTestCase):
    """Tests for quinteng/version.py"""

    def test_quinteng_version(self):
        """Test quinteng-version sets the correct version for chaoyue."""
        self.assertEqual(__version__, __quinteng_version__["quinteng-chaoyue"])
