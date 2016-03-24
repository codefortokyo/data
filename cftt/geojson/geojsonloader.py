# -*- coding: utf-8 -*-

import os
import re
import json
import collections
import zipfile
import urllib2

from .. common import base
from .. common import util
from .. feature.featurecollection import FeatureCollection


class GeoJSONLoader(collections.Callable, base.BaseAttribute):
    def __init__(self, **kwargs):
        super(GeoJSONLoader, self).__init__()
        self.attr(kwargs)

    def __call__(self, x):
        nonself = GeoJSONLoader(**self.attribute_items())
        return nonself._load(x)

    def _load(self, x):
        """Return FeatureCollection.
        If x is an object, then it just try to convert x to FeatureCollection.
        If x is a file-like object, it reads the content then try to convert
        the content to FeatureCollection. If x is a basestring object, it try
        to open it then read the content and try to convert to
        FeatureCollection. File path and http URL are supported.

        :param x:
        """
        if x is None:
            return FeatureCollection()
        if isinstance(x, FeatureCollection):
            return x
        if util.is_string(x):
            if util.is_url(x):
                return self._load_from_url(x)
            if os.path.isdir(x):
                return self._load_from_directory(x)
            if re.match('.*\.(geo)?json$', x):
                return self._load_from_json_file(x)
            if zipfile.is_zipfile(x):
                return self._load_from_zip_file(x)
            return self._load_from_string(x)
        if util.is_readable(x):
            return self._load_from_readable(x)
        if util.is_map(x):
            return self._load_from_object(x)
        raise Exception('Unknown input format')

    def _load_from_readable(self, x):
        return self._load_from_string(x.read())

    def _load_from_object(self, x):
        """Load from object. Return FeatureCollection.

        :param x: mapping object
        """
        return FeatureCollection(x).attr(self.attribute_items())

    def _load_from_string(self, x):
        """Load from JSON-formatted string. Return FeatureCollection.

        :param x: string
        """
        return self._load_from_object(json.loads(x))

    def _load_from_json_file(self, x):
        """Load from JSON-formatted file. Return FeatureCollection.

        :param x: file path
        """
        with open(x, 'r') as f:
            return self._load_from_string(f.read())

    def _load_from_url(self, x):
        """Load from directory. Return FeatureCollection including all the
        possible files.

        :param x: string
        """
        with util.ReopenableTempFile() as tmp:
            self.attr('original-url', x)
            resource = urllib2.urlopen(x)
            tmp.write(resource.read())
            tmp.close()
            if zipfile.is_zipfile(tmp.name):
                return self._load_from_zip_file(tmp.name)
            return self._load_from_json_file(tmp.name)

    def _load_from_directory(self, x):
        """Load from directory. Return FeatureCollection including all the
        possible files.

        :param x: string
        """
        res = FeatureCollection()
        for f in os.listdir(x):
            try:
                res += self(os.path.join(x, f))
            except:
                pass
        res.attr('root-directory', x)
        return res

    def _load_from_zip_file(self, x):
        """Load from zip file. Return FeatureCollection. Try to read files in
        the json files as much as possible.

        :param x: file path
        """

        with zipfile.ZipFile(x, 'r') as f:
            res = FeatureCollection()
            for zn in f.namelist():
                try:
                    res += self(f.open(zn))
                except:
                    pass
            res.attr('zip-name', x)
            return res
