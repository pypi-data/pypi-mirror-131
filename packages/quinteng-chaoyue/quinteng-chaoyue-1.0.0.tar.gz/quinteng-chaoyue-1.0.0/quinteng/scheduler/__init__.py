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

"""
===========================================
Circuit Scheduler (:mod:`quinteng.scheduler`)
===========================================

.. currentmodule:: quinteng.scheduler

A circuit scheduler compiles a circuit program to a pulse program.

.. autosummary::
   :toctree: ../stubs/

   schedule_circuit
   ScheduleConfig

.. automodule:: quinteng.scheduler.methods
"""
from quinteng.scheduler import schedule_circuit
from quinteng.scheduler.config import ScheduleConfig
from quinteng.scheduler.utils import measure, measure_all
