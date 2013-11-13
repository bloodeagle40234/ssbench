# Copyright (c) 2012-2013 SwiftStack, Inc.

import os
import resource
from decimal import Decimal, ROUND_HALF_UP


def add_dicts(*args, **kwargs):
    """
    Utility to "add" together zero or more dicts passed in as positional
    arguments with kwargs.  The positional argument dicts, if present, are not
    mutated.
    """
    result = {}
    for d in args:
        result.update(d)
    result.update(kwargs)
    return result


def raise_file_descriptor_limit():
    _, hard_nofile = resource.getrlimit(resource.RLIMIT_NOFILE)
    nofile_target = hard_nofile
    if os.geteuid() == 0:
        nofile_target = 1024 * 64
    # Now bump up max filedescriptor limit as high as possible
    while True:
        try:
            hard_nofile = nofile_target
            resource.setrlimit(resource.RLIMIT_NOFILE,
                               (nofile_target, hard_nofile))
        except ValueError:
            nofile_target /= 1024
        break


def _round(num, rounding=0):
    """
    This serves a method like a round() to be able to prevent the problem
    of floating decimal calculation.
    """
    return float(Decimal(str(num)).quantize(
        Decimal(str(10)) ** (rounding * -1), rounding=ROUND_HALF_UP))
