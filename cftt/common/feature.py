# -*- coding: utf-8 -*-

import sys
import os

import json

import collections

from shapely.geometry.point import BaseGeometry
from shapely.geometry import shape, mapping
from shapely.ops import cascaded_union

import util


class Feature(object):
    """単一の feature を扱うためのクラス
    """
    def __init__(self, data):
        """feature を構成する

        :param data: 'geometry' と 'properties' を属性に持った Mapping オブジェクト
        """
        self.load(data)

    def load(self, data):
        """data を元に feature を構成する

        :param data: 'geometry' と 'properties' を属性に持った Mapping オブジェクト
        """
        if isinstance(data, Feature):
            self.geometry = data.geometry
            self.properties = data.properties
            self.attributes = data.attributes
        else:
            self.geometry = data['geometry']
            self.properties = data['properties']
            self.attributes = {
                k: v for k, v in data.items()
                if k not in set(('geometry', 'properties', 'type'))
            }
        return self

    def dump(self):
        """このインスタンスを表す、json.dumpsなどでダンプ可能なオブジェクトを返す
        """
        return dict({u'type': u'Feature',
                     u'geometry': util.rec_decode(mapping(self._geometry)),
                     u'properties': self._properties}, **self._attributes)

    @property
    def properties(self):
        """このインスタンスの properties オブジェクト自体を返す
        """
        return self._properties

    @properties.setter
    def properties(self, x):
        """このインスタンスの properties を設定する

        :param x: Mapping オブジェクト
        """
        if not util.is_map(x):
            raise Exception('properties must be an instance of Mapping')
        self._properties = util.rec_decode(x)
        return self

    @property
    def geometry(self):
        """このインスタンスの geometry オブジェクト自体を返す
        """
        return self._geometry

    @geometry.setter
    def geometry(self, x):
        """このインスタンの geometry を設定する

        :param x: shape か shape に変換可能な Mapping オブジェクト
        """
        if isinstance(x, BaseGeometry):
            self._geometry = x
        elif util.is_map(x):
            self._geometry = shape(x)
        else:
            raise Exception('geometry must be an instance of shape')
        return self

    @property
    def attributes(self):
        """このインスタンスのその他の属性の Mapping オブジェクトを返す
        """
        return self._attributes

    @attributes.setter
    def attributes(self, x):
        """このインスタンスのその他の属性を設定する

        :param x: Mapping オブジェクト
        """
        if not util.is_map(x):
            raise Exception('attributes must be an instance of Mapping')
        self._attributes = util.rec_decode(x)
        return self

    def property(self, *x):
        """properties を set/get する。
        property('id') id 属性の値を取得する
        property('id', 'a123') id 属性の値を a123 に設定する

        :param x: 単一の値、list, dict, set, tupleまたはキーとヴァリューのペア
        """
        if len(x) == 0:
            return self
        if len(x) == 1:
            if util.is_map(x[0]):
                for k, v in util.rec_decode(x[0]).items():
                    self.property(k, v)
                return self
            if isinstance(x[0], collections.Set):
                return {k: self.property(k) for k in util.rec_decode(x[0])}
            if util.is_array(x[0]):
                return util.cons_array(
                    (self.property(k) for k in util.rec_decode(x[0])),
                    x[0].__class__, tuple)
            k = util.safe_decode(x[0])
            if not util.is_string(x[0]):
                k = unicode(x[0])
            if k in self._properties:
                return self._properties[k]
            return None
        k = util.safe_decode(x[0])
        if not util.is_string(x[0]):
            k = unicode(x[0])
        v = util.rec_decode(x[1])
        if v is None:
            if k in self._properties:
                del self._properties[k]
            return self
        self._properties[k] = v
        return self

    def attr(self, *x):
        """attributes を set/get する。
        attr('id') id 属性の値を取得する
        attr('id', 'a123') id 属性の値を a123 に設定する

        :param x: 単一の値、list, dict, set, tupleまたはキーとヴァリューのペア
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


class FeatureCollection(collections.MutableSequence):
    def __init__(self, x):
        super(FeatureCollection, self).__init__()
        self._features = []
        self._attributes = {}
        self.load(x)

    def load(self, x):
        """Load an instance from FeatureCollection or a Mapping object
        with 'features' attribute.
        """
        if isinstance(x, FeatureCollection):
            self._features = x._features
            self._attributes = x._attributes
        elif util.is_map(x):
            self._attributes = util.rec_decode({
                k: v for k, v in x.items()
                if k not in set(('features', 'type'))})
            self._features = [Feature(y) for y in x['features']]
        return self

    def dump(self):
        """Return dict object represents this instance.
        """
        return util.rec_decode(dict({
            'type': 'FeatureCollection',
            'features': [f.dump() for f in self._features]
        }, **self._attributes))

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

    def aggregate(self, keys=None, property=None, attribute=None):
        """Return another FeatureCollection whose features are mereged
        according to the result of the keys function. property and attribute
        are used when features are reduced.

        :param keys: a function takes properties and attributes of the feature
        as arguments.
        :param property: a function takes keys and a tuple of properties
        :param attribute: a function takes keys and a tuple of attriutes
        """
        temp = {}

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
