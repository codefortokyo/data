# -*- coding: utf-8 -*-

import sys
import os
import json
import collections

from shapely.geometry.point import BaseGeometry
from shapely.geometry import shape, mapping
from shapely.ops import cascaded_union

from .. common import util
from .. common import base


class Feature(base.BaseAttribute, base.BaseProperty):
    """Class for single feature. Handle `geometry`, `properties` and `attributes`
    """
    def __init__(self, data=None):
        """Construct a feature from data

        :param data: a map with `geometry` and `properties` or a Feature
        """
        super(Feature, self).__init__()
        self.load(data)

    def load(self, data=None):
        """Construct a feature from the data

        :param data: a map with `geometry` and `properties` or a Feature
        """
        if data is None:
            self.geometry = None
            self.properties = {}
            self.attributes = {}
        elif isinstance(data, Feature):
            self.geometry = data.geometry
            self.clear_properties()
            self.properties = data.properties
            self.clear_attributes()
            self.attributes = data.attributes
        else:
            self.geometry = data['geometry']
            self.properties = data['properties']
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
                         'geometry': None if self._geometry is None else
                         mapping(self._geometry),
                         'properties': self._properties.dump(encoding=encoding)
                         }, **self._attributes.dump(encoding=encoding))
        return dict({u'type': u'Feature',
                     u'geometry': util.rec_decode(
                        None if self._geometry is None else
                        mapping(self._geometry)),
                     u'properties': self._properties.dump()},
                    **self._attributes.dump())

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
        if x is None:
            self._geometry = None
        elif isinstance(x, BaseGeometry):
            self._geometry = x
        elif util.is_map(x):
            self._geometry = shape(x)
        else:
            raise Exception('geometry must be an instance of shape')
        return self


class FeatureCollection(collections.MutableSequence, base.BaseAttribute):
    def __init__(self, *args):
        super(FeatureCollection, self).__init__()
        self._features = []
        self.load(*args)

    def load(self, *args):
        """Load an instance from FeatureCollection or a Mapping object
        with 'features' attribute.
        """
        self.clear_attributes()
        self._features = []
        for x in args:
            if isinstance(x, FeatureCollection):
                self._features += x._features
                self.attr(x.attributes)
            elif util.is_map(x):
                self.attr({
                    k: v for k, v in x.items()
                    if k not in set(('features', 'type'))})
                self._features += [Feature(y) for y in x['features']]
        return self

    def dump(self, encoding=None):
        """Return dict object represents this instance.
        """
        if encoding is not None:
            return dict({
                'type': 'FeatureCollection',
                'features': [f.dump(encoding=encoding) for f in self._features]
            }, **util.rec_encode(self._attributes.dump(encoding=encoding),
                                 encoding=encoding))
        return dict({
            u'type': u'FeatureCollection',
            u'features': [f.dump() for f in self._features]
        }, **util.rec_decode(self._attributes.dump()))

    def filter(self, f):
        """Return generator of features filtered by `f`

        :param f: function takes a feature as an argument.
        """
        for feature in self:
            if f(feature):
                yield feature

    def map(self, f):
        """Return generator of features applied f

        :param f: function takes a feature as an argument.
        """
        for feature in self:
            yield Feature(f(feature))

    def aggregate(self, key=lambda f: tuple(f.property_values()),
                  prop=lambda k, fl, i: fl[0].property_items(),
                  attr=lambda k, fl, i: dict(fl[0].attribute_items(),
                                             **{'id': i}),
                  geom=lambda k, fl, i: cascaded_union(
                                        map(lambda x: x.geometry, fl)),
                  sort=lambda k: k, reverse=False,
                  cattr=lambda s: s._attributes):
        """Return another FeatureCollection whose features are mereged
        according to the result of the keys function. property and attribute
        are used when features are reduced.

        :param key: function takes a feature as an argument.
        :param prop: function takes key, list of features and index
        :param attr: function takes key, list of features and index
        :param geom: function takes key, list of features and index
        :param cattr: function takes self
        """
        temp = dict()
        for f in self:
            k = tuple(key(f))
            if k not in temp:
                temp[k] = []
            temp[k].append(f)
        temp = sorted([(k, v) for k, v in temp.items()],
                      reverse=reverse,
                      key=lambda x: sort(x[0]))
        return self.__class__(dict({
            'features': [
                Feature(dict({
                    'properties': prop(t[0], t[1], i),
                    'geometry': geom(t[0], t[1], i)
                }, **attr(t[0], t[1], i))) for i, t in enumerate(temp)
            ]
        }, **cattr(self)))

    def __iter__(self):
        return self._features.__iter__()

    def __getitem__(self, i):
        return self._features.__getitem__(i)

    def __setitem__(self, i, x):
        return self._features.__setitem__(i, Feature(x))

    def __delitem__(self, i):
        return self._features.__delitem__(i)

    def __len__(self):
        return self._features.__len__()

    def insert(self, i, x):
        return self._features.insert(i, Feature(x))

    def __iadd__(self, other):
        self.attr(other.attributes)
        self._features += other._features
        return self

    def __add__(self, other):
        res = FeatureCollection(self)
        res += other
        return res
