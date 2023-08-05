# This code is part of Quinteng.
#
# (C) Copyright IBM 2017.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=wrong-import-position

"""Main Quinteng public functionality."""

import pkgutil
import sys
import warnings

# quinteng errors operator
from quinteng.exceptions import QuintengError, MissingOptionalLibraryError

# The main quinteng operators
from quinteng.circuit import ClassicalRegister
from quinteng.circuit import QuantumRegister
from quinteng.circuit import AncillaRegister
from quinteng.circuit import QuantumCircuit

# user config
from quinteng import user_config as _user_config

# The quinteng.extensions.x imports needs to be placed here due to the
# mechanism for adding gates dynamically.
import quinteng.extensions
import quinteng.circuit.measure
import quinteng.circuit.reset

# Allow extending this namespace. Please note that currently this line needs
# to be placed *before* the wrapper imports or any non-import code AND *before*
# importing the package you want to allow extensions for (in this case `backends`).
__path__ = pkgutil.extend_path(__path__, __name__)

# Please note these are global instances, not modules.
from quinteng.providers.basicaer import BasicAer

_config = _user_config.get_config()

# Moved to after IBMQ and Aer imports due to import issues
# with other modules that check for IBMQ (tools)
from quinteng.execute_function import execute  # noqa
from quinteng.compiler import transpile, assemble, schedule, sequence  # noqa

from .version import __version__  # noqa
from .version import QuintengVersion  # noqa


__quinteng_version__ = QuintengVersion()


class AerWrapper:
    """Lazy loading wrapper for Aer provider."""

    def __init__(self):
        self.aer = None

    def __bool__(self):
        if self.aer is None:
            try:
                from quinteng.providers import aer

                self.aer = aer.Aer
            except ImportError:
                return False
        return True

    def __getattr__(self, attr):
        if not self.aer:
            try:
                from quinteng.providers import aer

                self.aer = aer.Aer
            except ImportError as ex:
                raise MissingOptionalLibraryError(
                    "quinteng-aer", "Aer provider", "pip install quinteng-aer"
                ) from ex
        return getattr(self.aer, attr)


class IBMQWrapper:
    """Lazy loading wrapper for IBMQ provider."""

    def __init__(self):
        self.ibmq = None

    def __bool__(self):
        if self.ibmq is None:
            try:
                from quinteng.providers import ibmq

                self.ibmq = ibmq.IBMQ
            except ImportError:
                return False
        return True

    def __getattr__(self, attr):
        if not self.ibmq:
            try:
                from quinteng.providers import ibmq

                self.ibmq = ibmq.IBMQ
            except ImportError as ex:
                raise MissingOptionalLibraryError(
                    "quinteng-ibmq-provider", "IBMQ provider", "pip install quinteng-ibmq-provider"
                ) from ex
        return getattr(self.ibmq, attr)


Aer = AerWrapper()
IBMQ = IBMQWrapper()

__all__ = [
    "Aer",
    "AncillaRegister",
    "BasicAer",
    "ClassicalRegister",
    "IBMQ",
    "MissingOptionalLibraryError",
    "QuintengError",
    "QuantumCircuit",
    "QuantumRegister",
    "assemble",
    "execute",
    "schedule",
    "sequence",
    "transpile",
]
