# -*- coding: utf-8 -*-

import sys
import os
import json
import collections

from shapely.geometry.point import BaseGeometry
from shapely.geometry import shape, mapping

from .. common import util


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
