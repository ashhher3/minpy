#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Policy for selecting appropriate function to call."""
import itertools
import functools
import operator
from .utils import log
from . import array
from . import registry
from . import array_variants as variants

logger = log.get_logger(__name__)

class AmbiguousPolicyError(ValueError):
    pass

class Policy(object):
    """Policy interface """
    def decide(self, candidates, *args, **kwargs):
        raise AmbiguousPolicyError('Unimplemented')


class PreferMXNetPolicy(Policy):
    """Perfer using MXNet functions."""
    def decide(self, candidates, *args, **kwargs):
        if variants.FunctionType.MXNET in candidates.keys():
            return variants.FunctionType.MXNET
        else:
            return variants.FunctionType.NUMPY

default_policy = Policy()

def resolve_name(name, args, kwargs, reg, policy=default_policy):
    """Resolve a function name.

    Args:
        name: Name of the function.
        args: Arguments.
        kwargs: Keyword arguments.
        reg: Registry for functions.
        policy: Resolving policy.

    Returns:
        A function after resolution.
    """
    available = reg.iter_available_types(name)
    preference = policy.decide(available, args, kwargs)
    return reg.get(name, preference)
