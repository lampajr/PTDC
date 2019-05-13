"""
Python Twitter Data Collector library initialization

:copyright: Copyright since 2019 Lamparelli Andrea, all rights reserved
:license: MIT, see LICENSE for more details.
"""
import logging

from ptdc.collector import Collector, AccountCollector, StatusCollector, default_statuses_features, \
    default_account_timeline_features, default_account_features
from ptdc.streamer import OnlineStreamer
from ptdc.support import authenticate

__version__ = '1.2.9'
__author__ = 'Andrea Lamparelli'
__license__ = "MIT"

__all__ = [
    'AccountCollector',
    'StatusCollector',
    'Collector',
    'default_account_timeline_features',
    'default_statuses_features',
    'default_account_features',
    'OnlineStreamer',
    'authenticate',
    '__version__'
]

logging.basicConfig(level=logging.WARNING, format='%(levelname)s:%(module)s:%(message)s')
