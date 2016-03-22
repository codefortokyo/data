# -*- coding: utf-8 -*-

import sys
import os
import json
import collections

from shapely.geometry.point import BaseGeometry
from shapely.geometry import shape, mapping

from .. common import util
from .. common import base


class Feature(base.BaseAttribute, base.BaseProperty):
    """Class for single feature. Handle `geometry`, `properties` and `attributes`
    """
    def __init__(self, data):
        """Construct a feature from data

        :param data: a map with `geometry` and `properties` or a Feature
        """
        super(Feature, self).__init__()
        self.load(data)

    def load(self, data):
        """Construct a feature from the data

        :param data: a map with `geometry` and `properties` or a Feature
        """
        if isinstance(data, Feature):
            self.geometry = data.geometry
            self.clear_properties()
            self.property(data.property_items())
            self.clear_attributes()
            self.attr(data.attribute_items())
        else:
            self.geometry = data['geometry']
            self.property(data['properties'])
            self.attributes = {
                k: v for k, v in data.items()
                if k not in set(('geometry', 'properties', 'type'))
            }
        return self

    def dump(self, encoding=None):
        """Return an object represents this instance.

        :param encoding: string represents encoding. default unicode
        """
        if encoding is not None:
            return dict({'type': 'Feature',
                         'geometry': mapping(self._geometry),
                         'properties': util.rec_encode(self._properties,
                                                       encoding=encoding)},
                        **util.rec_encode(self._attributes, encoding=encoding))
        return dict({u'type': u'Feature',
                     u'geometry': util.rec_decode(mapping(self._geometry)),
                     u'properties': self._properties}, **self._attributes)

    @property
    def geometry(self):
        """Return `geometry` of this instance
        """
        return self._geometry

    @geometry.setter
    def geometry(self, x):
        """Set `geometry` of this instance

        :param x: shape or a Map compatible with shape.
        """
        if isinstance(x, BaseGeometry):
            self._geometry = x
        elif util.is_map(x):
            self._geometry = shape(x)
        else:
            raise Exception('geometry must be an instance of shape')
        return self
