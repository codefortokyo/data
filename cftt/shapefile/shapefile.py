# -*- coding: utf-8 -*-

import sys
import os
import json
import urllib2
import collections
import re
import tempfile
import zipfile
import warnings

from shapely.geometry import shape, mapping
from shapely.ops import cascaded_union
import fiona
from fiona.crs import to_string

from .. common import util
from .. common.feature import Feature


class ShapeFile(collections.Iterable):
    def __init__(self, x):
        super(ShapeFile, self).__init__()
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

    def _load_from_fiona(self, f):
        """Load from fiona object. Return self.

        :param f: fiona object
        """
        self.__crs = to_string(f.crs)
        self.__attributes = {}
        for s in f:
            self.__features.append(Feature(s))

    def _load_from_zip(self, zip, name=None):
        """Load the zipped shape file from zip. Return self.

        :param zip: zip
        """
        if name is not None:
            with fiona.open(
                    (lambda n: n if n.startswith('/') else '/' + n)(name),
                    vfs='zip://' + zip) as f:
                return self._load_from_fiona(f)
        else:
            with zipfile.ZipFile(zip) as z:
                names = filter(
                    lambda x: re.match('.*\.shp$', x, flags=re.IGNORECASE),
                    z.namelist())
                if len(names) == 0:
                    warnings.warn('no shape file found')
                    return self
                if len(names) > 1:
                    warnings.warn('multiple shape files found: load ' +
                                  names[0] + ' only.')
                return self._load_from_zip(zip, names[0])

    def _load_from_url(self, url):
        """Load the zipped shape file from url. Return self.

        :param url: url to the zipped ShapeFile.
        """
        with tempfile.NamedTemporaryFile() as tmp:
            resource = urllib2.urlopen(url)
            tmp.write(resource.read())
            resource.close()
            return self._load_from_zip(tmp.name)

    def _load_from_shp(self, shp):
        """Load the shape file from shp. Return self.

        :param shp: string
        """
        with fiona.drivers():
            with fiona.open(shp) as source:
                return self._load_from_fiona(source)

    def dump(self):
        """Return dict object represents this instance.
        """
        return util.rec_decode(
            dict({
                'type': 'FeatureCollection',
                'features': [f.dump() for f in self.__features]
            }, **dict(
                self.__attributes,
                **((lambda x: {} if x is None else {'crs': x})(self.__crs))
            ))
        )

    def __iter__(self):
        return self.__features.__iter__()

    def __len__(self):
        return self.__features.__len__()
