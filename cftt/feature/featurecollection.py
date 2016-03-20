# -*- coding: utf-8 -*-

import sys
import os
import json
import collections

from shapely.ops import cascaded_union

from feature import Feature
from .. common import util


class FeatureCollection(collections.MutableSequence):
    def __init__(self, *args):
        super(FeatureCollection, self).__init__()
        self._features = []
        self._attributes = {}
        self.load(*args)

    def load(self, *args):
        """Load an instance from FeatureCollection or a Mapping object
        with 'features' attribute.
        """
        for x in args:
            if isinstance(x, FeatureCollection):
                self._features += x._features
                self.attr(x._attributes)
            elif util.is_map(x):
                self.attr(util.rec_decode({
                    k: v for k, v in x.items()
                    if k not in set(('features', 'type'))}))
                self._features += [Feature(y) for y in x['features']]
        return self

    def dump(self, encoding=None):
        """Return dict object represents this instance.
        """
        if encoding is not None:
            return dict({
                'type': 'FeatureCollection',
                'features': [f.dump(encoding=encoding) for f in self._features]
            }, **util.rec_encode(self._attributes, encoding=encoding))
        return dict({
            u'type': u'FeatureCollection',
            u'features': [f.dump() for f in self._features]
        }, **util.rec_decode(self._attributes))

    def attr(self, *x):
        """set/get attributes.

        attr('id'): Return value of 'id'

        attr('id', 'a123'): set value of 'id' to 'a123' then return self

        :param x: single key, list, dict, set, tuple or key-value pair
        """
        if len(x) == 0:
            return self
        if len(x) == 1:
            if util.is_map(x[0]):
                for k, v in util.rec_decode(x[0]).items():
                    self.attr(k, v)
                return self
            if isinstance(x[0], collections.Set):
                return {k: self.attr(k) for k in util.rec_decode(x[0])}
            if util.is_array(x[0]):
                return util.cons_array(
                    (self.attr(k) for k in util.rec_decode(x[0])),
                    x[0].__class__, tuple)
            k = util.safe_decode(x[0])
            if not util.is_string(x[0]):
                k = unicode(x[0])
            if k in self._attributes:
                return self._attributes[k]
            return None
        k = util.safe_decode(x[0])
        if not util.is_string(x[0]):
            k = unicode(x[0])
        v = util.rec_decode(x[1])
        if v is None:
            if k in self._attributes:
                del self._attributes[k]
            return self
        self._attributes[k] = v
        return self

    def aggregate(self, key=lambda f: tuple(f.properties.values()),
                  prop=lambda k, fl, i: fl[0].properties,
                  attr=lambda k, fl, i: dict(fl[0].attributes, **{'id': i}),
                  geom=lambda k, fl, i: cascaded_union(
                                        map(lambda x: x.geometry, fl)),
                  sort=lambda k: k, reverse=False,
                  cattr=lambda s: s.attributes):
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
        for f in self.features:
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

    @property
    def attributes(self):
        """Return attributes of this instance.
        """
        return self._attributes

    @attributes.setter
    def attributes(self, x):
        """Set attributes of this instance. Return self.

        :param x: mapping
        """
        if not util.is_map(x):
            raise Exception('attributes must be a mapping.')
        self._attributes = util.rec_decode(x)
        return self

    @property
    def features(self):
        """Return features
        """
        return self._features

    @features.setter
    def features(self, x):
        """Set features of this instance. Return self.

        :param x: linear iterable
        """
        if not util.is_array(x):
            raise Exception('features must be a linear iterable container.')
        self._features = [Feature(y) for y in x]
        return self

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