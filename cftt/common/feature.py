# -*- coding: utf-8 -*-

import sys
import os

import json

import collections

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
        self.__geometry = shape(data['geometry'])
        self.__properties = util.rDecode(data['properties'])
        self.__attributes = util.rDecode({
            k: v for k, v in data.items()
            if k not in set(('geometry', 'properties', 'type'))
        })
        return self

    def dump(self):
        """このインスタンスを表す、json.dumpsなどでダンプ可能なオブジェクトを返す
        """
        return dict({u'type': u'Feature',
                     u'geometry': util.rDecode(mapping(self.__geometry)),
                     u'properties': self.__properties}, **self.__attributes)

    @property
    def properties(self):
        """このインスタンスの properties オブジェクト自体を返す
        """
        return self.__properties

    @properties.setter
    def properties(self, x):
        """このインスタンスの properties を設定する

        :param x: Mapping オブジェクト
        """
        if not util.isMapping(x):
            raise Exception('properties must be an instance of Mapping')
        self.__properties = rDecode(x)
        return self

    @property
    def geometry(self):
        """このインスタンスの geometry オブジェクト自体を返す
        """
        return self.__geometry

    @geometry.setter
    def geometry(self, x):
        """このインスタンの geometry を設定する

        :param x: shape か shape に変換可能な Mapping オブジェクト
        """
        if isinstance(x, shape):
            self.__geometry = x
        elif util.isMapping(x):
            self.__geometry = shape(x)
        else:
            raise Exception('geometry must be an instance of shape')
        return self

    @property
    def attributes(self):
        """このインスタンスのその他の属性の Mapping オブジェクトを返す
        """
        return self.__attributes

    @attributes.setter
    def attributes(self, x):
        """このインスタンスのその他の属性を設定する

        :param x: Mapping オブジェクト
        """
        if not util.isMapping(x):
            raise Exception('attributes must be an instance of Mapping')
        self.__attributes = rDecode(x)
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
            if util.isMapping(x[0]):
                for k, v in util.rDecode(x[0]):
                    self.property(k, v)
                return self
            if isinstance(x[0], collections.Set):
                return {k: self.property(k) for k in util.rDecode(x[0])}
            if util.isIterable(x[0]):
                res = tuple(self.property(k) for k in util.rDecode(x[0]))
                try:
                    return x[0].__class__(res)
                except:
                    return res
            k = util.safeDecode(x[0])
            if not util.isString(x[0]):
                k = unicode(x[0])
            if k in self.__properties:
                return self.__properties[k]
            return None
        k = util.safeDecode(x[0])
        if not util.isString(x[0]):
            k = unicode(x[0])
        v = util.safeDecode(x[1])
        if v is None:
            if k in self.__properties:
                del self.__properties[k]
            return self
        self.__properties[k] = v
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
            if util.isMapping(x[0]):
                for k, v in util.rDecode(x[0]):
                    self.attr(k, v)
                return self
            if isinstance(x[0], collections.Set):
                return {k: self.attr(k) for k in util.rDecode(x[0])}
            if util.isIterable(x[0]):
                res = tuple(self.attr(k) for k in util.rDecode(x[0]))
                try:
                    return x[0].__class__(res)
                except:
                    return res
            k = util.safeDecode(x[0])
            if not util.isString(x[0]):
                k = unicode(x[0])
            if k in self.__attributes:
                return self.__attributes[k]
            return None
        k = util.safeDecode(x[0])
        if not util.isString(x[0]):
            k = unicode(x[0])
        v = util.safeDecode(x[1])
        if v is None:
            if k in self.__attributes:
                del self.__attributes[k]
            return self
        self.__attributes[k] = v
        return self

    def isMatch(self, condition):
        """このインスタンスの properties が condition に一致しているかどうか返す

        :param condition: 一つの引数（propertiesが渡される）を取る関数
        """
        return condition(self.__properties)

    def join(self, d):
        """d のキーヴァリューの組をこのインスタンスの properties に追加する

        :param d: Mapping オブジェクト
        """
        self.__properties = dict(self.__properties, **d)
        return self
