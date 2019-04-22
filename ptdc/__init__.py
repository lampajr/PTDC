"""
Python Twitter Data Collector library initialization

:copyright: Copyright since 2019 Lamparelli Andrea, all rights reserved
:license: MIT, see LICENSE for more details.
"""
import logging

from ptdc.collector import Collector
from ptdc.streamer import Streamer, OnlineStreamer, OnlineStatusStreamer
from ptdc.support import authenticate, multiple_authentication

__version__ = '0.1.9'
__author__ = 'Andrea Lamparelli'
__license__ = "MIT"

__all__ = [
    'Collector',
    'data',
    'Streamer',
    'OnlineStreamer',
    'OnlineStatusStreamer',
    'authenticate',
    'multiple_authentication',
    '__version__'
]

logging.basicConfig(level=logging.WARNING, format='%(levelname)s:%(module)s.%(funcName)s.%(lineno)d:%(message)s')
