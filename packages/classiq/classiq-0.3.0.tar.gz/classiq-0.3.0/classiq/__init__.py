"""Classiq SDK."""

import classiq.logger as logger  # noqa: F401
from classiq._version import VERSION as _VERSION
from classiq.async_utils import enable_jupyter_notebook, is_notebook as _is_notebook
from classiq.authentication.authentication import authenticate  # noqa: F401
from classiq.client import configure  # noqa: F401
from classiq.executor import Executor  # noqa: F401
from classiq.generator import Generator  # noqa: F401
from classiq.quantum_register import *  # noqa: F401, F403

__version__ = _VERSION


if _is_notebook():
    enable_jupyter_notebook()
