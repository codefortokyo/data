# -*- coding: utf-8 -*-

import collections
import __builtin__
import copy

from .. common import util
from .. common import base


class BaseStream(base.BaseAttribute, collections.abc.Iterator):
    def __init__(self):
        super(BaseStream, self).__init__()
