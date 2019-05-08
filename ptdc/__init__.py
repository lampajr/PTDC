"""
Python Twitter Data Collector library initialization

:copyright: Copyright since 2019 Lamparelli Andrea, all rights reserved
:license: MIT, see LICENSE for more details.
"""
import logging

from ptdc.collector import Collector, AccountCollector, StatusCollector
from ptdc.streamer import OnlineStreamer
from ptdc.support import authenticate

__version__ = '1.0.0'
__author__ = 'Andrea Lamparelli'
__license__ = "MIT"

__all__ = [
    'AccountCollector',
    'StatusCollector',
    'Collector',
    'data',
    'OnlineStreamer',
    'authenticate',
    '__version__'
]

logging.basicConfig(level=logging.WARNING, format='%(levelname)s:%(module)s.%(funcName)s.%(lineno)d:%(message)s')
