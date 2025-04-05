"""
Alias module for backward compatibility with pysnooper.
This module re-exports everything from snooper_ai.
"""
import sys
import warnings

# Re-export everything from snooper_ai
from snooper_ai import *
from snooper_ai import (
    __version__,
    tracer,
    utils,
    variables,
    pycompat,
)

# Create aliases for submodules
sys.modules['pysnooper.tracer'] = tracer
sys.modules['pysnooper.utils'] = utils
sys.modules['pysnooper.variables'] = variables
sys.modules['pysnooper.pycompat'] = pycompat

# Show a deprecation warning when using the old import
warnings.warn(
    "The 'pysnooper' package name is deprecated and will be removed in a future version. "
    "Please use 'snooper_ai' instead.",
    DeprecationWarning,
    stacklevel=2
) 