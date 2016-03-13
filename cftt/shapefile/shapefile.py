# -*- coding: utf-8 -*-

import sys
import os
import json
import urllib2
import collections
import re

from shapely.geometry import shape, mapping
from shapely.ops import cascaded_union
import fiona
from fiona.crs import to_string

from .. common import util
from .. common.feature import Feature


class ShapeFile(collections.Iterable):
    def __init__(self, x):
        super(shapeHandler, self).__init__()
        self.__features = []
        self.__attributes = {}
        self.__crs = None
        self.load(x)

    def load(self, x):
        if isinstance(x, ShapeFile):
            self.__features = x.__features
            self.__attributes = x.__attributes
            self.__crs = x.__crs
            return self
        elif util.is_string(x):
            if util.is_url(x):
                return self._load_from_url(x)
            elif re.match('.*\.shp$', x):
                return self._load_from_shp(x)
            elif re.match('.*\.zip$', x):
                return self._load_from_zip(x)
            else:
                raise Exception('Unknown input format')
        elif util.is_map(x):
            self.__attributes = util.rec_decode({
                k: v for k, v in x.items() if k not in set(('features', 'crs'))
            })
            if 'features' in x:
                self.__features = [Feature(s) for s in x['features']]
            if 'crs' in x:
                self.__crs = x['crs']
        else:
            raise Exception('Unknown input format')
        return self

    def _load_from_zip(self, zip):
        """Load the zipped shape file from zip. Return self.

        :param zip: zip
        """
        return self

    def _load_from_url(self, url):
        """Load the zipped shape file from url. Return self.

        :param url: url to the zipped ShapeFile.
        """
        return self

    def _load_from_shp(self, shp):
        """Load the shape file from shp. Return self.

        :param shp: string
        """
        with fiona.drivers():
            with fiona.open(shp) as source:
                crs = to_string(source.crs)
                for s in source:
                    self.__features.append(Feature(s))
        return self
