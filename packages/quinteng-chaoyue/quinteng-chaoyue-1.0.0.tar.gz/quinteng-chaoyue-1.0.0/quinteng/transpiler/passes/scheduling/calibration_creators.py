# This code is part of Quinteng.
#
# (C) Copyright IBM 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=unused-import

"""Calibration creators."""

import warnings
from quinteng.transpiler.passes.calibration import RZXCalibrationBuilder, RZXCalibrationBuilderNoEcho

# TODO remove this import after sufficient deprecation period

warnings.warn(
    "RZXCalibrationBuilder and RZXCalibrationBuilderNoEcho passes are moved to "
    "`quinteng.transpiler.passes.calibration.builders`. "
    "This import path is being deprecated.",
    DeprecationWarning,
)
