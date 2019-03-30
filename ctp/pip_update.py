#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import call
from pip._internal.utils.misc import get_installed_distributions

"""
pip 更新所有包
"""

for dist in get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)