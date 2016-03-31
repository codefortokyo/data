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
from .. common.reopenabletempfile import ReopenableTempFile


class ShapeLoader(collections.Callable, base.BaseAttribute):
    def __init__(self, encoding=None, **kwargs):
        super(ShapeLoader, self).__init__()
        self.attr(kwargs)
        self._encoding = encoding

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, x):
        self._encoding = x

    @encoding.deleter
    def encoding(self):
        self._encoding = None

    def __call__(self, x=None):
        nonself = ShapeLoader(**self._attributes)
        return nonself._load(x)

    def _aug_attr(self, f):
        for k, v in self.attributes.items():
            if util.is_callable(v):
                f.attributes[k] = v(f)
            else:
                f.attributes[k] = v
        return f

    def _load(self, x):
        """Return FeatureCollection. If x is

        :param x:
        """
        if x is None:
            return self._aug_attr(FeatureCollection())
        if isinstance(x, FeatureCollection):
            return self._aug_attr(FeatureCollection(x))
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
            return self._aug_attr(FeatureCollection(x))
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
        for k, v in self.attributes.items():
            if util.is_callable(v):
                a[k] = v(f)
            else:
                a[k] = v
        a['features'] = []
        for s in f:

            props = json.loads(json.dumps(s['properties']))
            print json.dumps(s['properties'])
            print props
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
                res = FeatureCollection()
                for name in names:
                    res += self._load_from_zip(zip, name)
                return res

    def _load_from_url(self, url):
        """Load the zipped shape file from url. Return FeatureCollection.

        :param url: url to the zipped ShapeLoader.
        """
        with ReopenableTempFile(suffix='.zip') as tmp:
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
            if self._encoding is None:
                with fiona.open(shp) as source:
                    self.attr('shp-name', shp)
                    return self._load_from_fiona(source)
            with fiona.open(shp, encoding=self._encoding) as source:
                self.attr('shp-name', shp)
                return self._load_from_fiona(source)
