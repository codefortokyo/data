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

import fiona
from fiona.crs import to_string

from .. common import util
from .. feature.feature import Feature
from .. feature.featurecollection import FeatureCollection
from .. common import base


class ShapeLoader(collections.Callable, base.BaseAttribute):
    def __init__(self, **kwargs):
        super(ShapeLoader, self).__init__()
        self.attr(kwargs)

    def __call__(self, x):
        nonself = ShapeLoader(**self._attributes)
        return nonself._load(x)

    def _load(self, x):
        """Return FeatureCollection. If x is

        :param x:
        """
        if isinstance(x, FeatureCollection):
            return x
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
            return FeatureCollection(x)
        raise Exception('Unknown input format')

    def _load_from_fiona(self, f):
        """Load from fiona object. Return FeatureCollection.

        :param f: fiona object
        """
        a = {}
        try:
            a['crs'] = to_string(f.crs)
        except:
            pass
        for k, v in self._attributes.items():
            if util.is_callable(v):
                a[k] = v(f)
            else:
                a[k] = v
        a['features'] = []
        for s in f:
            a['features'].append(Feature(s))
        return FeatureCollection(a)

    def _load_from_zip(self, zip, name=None):
        """Load the zipped shape file from zip. Return FeatureCollection.

        :param zip: zip file name.
        :param name: shape file name with path in the zip file.
        """
        if name is not None:
            fn = (lambda n: n if n.startswith('/') else '/' + n)(name)
            with fiona.open(fn, vfs='zip://' + zip) as f:
                self.attr('shp-name', fn)
                self.attr('zip-name', os.path.basename(zip))
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
        """Load the zipped shape file from url. Return FeatureCollection.

        :param url: url to the zipped ShapeLoader.
        """
        with util.ReopenableTempFile(suffix='.zip') as tmp:
            self.attr('original-url', url)
            resource = urllib2.urlopen(url)
            tmp.write(resource.read())
            tmp.close()
            return self._load_from_zip(tmp.name).attr('zip-name', url)

    def _load_from_shp(self, shp):
        """Load the shape file from shp. Return FeatureCollection.

        :param shp: string
        """
        with fiona.drivers():
            with fiona.open(shp) as source:
                self.attr('shp-name', shp)
                return self._load_from_fiona(source)
