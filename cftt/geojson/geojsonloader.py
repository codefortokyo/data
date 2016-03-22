# -*- coding: utf-8 -*-

import collections


class GeoJSONLoader(collections.Callable):
    def __init__(self, **kwargs):
        super(GeoJSONLoader, self).__init__()
