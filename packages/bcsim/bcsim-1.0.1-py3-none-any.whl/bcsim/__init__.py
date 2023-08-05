
"""
.. include:: ../../docs/intro.md
"""

__version__ = '1.0.1'

from .rail import Ball
from .rail import Rail
from .clocks import Clock
from .clocks import FastClock
from .tools import clear
from .tools import runSimulation

__pdoc__ = {}
__pdoc__['clocks.Clock.__str__'] = True
__pdoc__['rail.Rail.__eq__'] = True
