# This code is part of Quinteng.
#
# (C) Copyright IBM 2018, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
==========================================
App Provider (:mod:`quinteng.providers.app`)
==========================================

.. currentmodule:: quinteng.providers.app

Simulator Provider
==================

.. autosummary::
    :toctree: ../stubs/

    AppProvider

Simulator Backends
==================

.. autosummary::
    :toctree: ../stubs/

    AppSimulator
    PulseSimulator

Legacy Simulator Backends
=========================

.. autosummary::
    :toctree: ../stubs/

    QasmSimulator
    StatevectorSimulator
    UnitarySimulator

Exceptions
==========
.. autosummary::
   :toctree: ../stubs/

   AppError
"""

# https://github.com/Quinteng/quinteng-app/issues/1
# Because of this issue, we need to make sure that Numpy's OpenMP library is initialized
# before loading our simulators, so we force it using this ugly trick
import platform
if platform.system() == "Darwin":
    import numpy as np
    np.dot(np.zeros(100), np.zeros(100))
# ... ¯\_(ツ)_/¯

# pylint: disable=wrong-import-position
from .appprovider import AppProvider
from .jobs import AppJob, AppJobSet
from .apperror import AppError
from .backends import *
from . import library
from . import pulse
from . import noise
from . import utils
from .version import __version__

# Global instance to be used as the entry point for convenience.
App = AppProvider()  # pylint: disable=invalid-name
