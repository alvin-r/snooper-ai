# Copyright 2019 Ram Rachum and collaborators.
# This program is distributed under the MIT license.

from .tracer import Tracer as snoop
from .variables import Attrs, Exploding, Indices, Keys
import collections

__VersionInfo = collections.namedtuple('VersionInfo',
                                       ('major', 'minor', 'micro'))

__version__ = '0.0.2'
__version_info__ = __VersionInfo(*(map(int, __version__.split('.'))))

del collections, __VersionInfo # Avoid polluting the namespace

"""
snooper-ai - Debug your Python code with AI assistance.

A modern AI-powered debugger for Python that helps you understand your code's behavior.
"""

__version__ = '0.1.0'

from .tracer import Tracer

def snoop(*args, **kwargs):
    """
    Debug your Python code with AI assistance.
    
    This is a wrapper around PySnooper's functionality that adds AI analysis capabilities.
    Use the @snoop decorator or snoop() context manager to capture execution traces,
    then get AI-powered insights about your code's behavior.
    
    Example:
        @snoop()
        def your_function(x):
            ...
    """
    return Tracer(*args, **kwargs)
