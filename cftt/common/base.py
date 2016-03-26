# -*- coding: utf-8 -*-

import collections
import __builtin__

import util


class _DecodedDict(collections.MutableMapping):
    def __init__(self, *arg, **kwargs):
        super(_DecodedDict, self).__init__()
        self._elements = dict()
        self(dict(*arg, **kwargs))

    def __getitem__(self, key):
        if util.is_map(key):
            return util.cons_map(
                ((k, self.__getitem__(v)) for k, v in key.items()),
                key.__class__
            )
        if isinstance(key, collections.Set):
            return {k: self.__getitem__(k) for k in util.rec_decode(key)}
        if util.is_array(key):
            return util.cons_array(
                (self.__getitem__(k) for k in key),
                key.__class__
            )
        if util.is_string(key):
            k = util.safe_decode(key)
        else:
            k = unicode(key)
        if k in self._elements:
            return self._elements[k]
        return None

    def __setitem__(self, key, value):
        if util.is_map(key):
            return self.__setitem__(key.values(), value)
        if util.is_array(key):
            for k in key:
                self.__setitem__(k, value)
            return
        if value is None:
            self.__delitem__(key)
            return
        if util.is_string(key):
            k = util.safe_decode(key)
        else:
            k = unicode(key)
        self._elements[k] = util.rec_decode(value)
        return

    def __delitem__(self, key):
        if util.is_map(key):
            return self.__delitem__(key.values())
        if util.is_array(key):
            for k in key:
                self.__delitem__(k)
            return
        if util.is_string(key):
            k = util.safe_decode(key)
        else:
            k = unicode(key)
        if k in self._elements:
            del self._elements[k]
        return

    def __iter__(self):
        return self._elements.__iter__()

    def __len__(self):
        return self._elements.__len__()

    def __call__(self, *x):
        if len(x) == 0:
            return self
        if len(x) == 1:
            if util.is_map(x[0]):
                for k, v in x[0].items():
                    self(k, v)
                return self
            return self.__getitem__(x[0])
        self.__setitem__(x[0], x[1])
        return self


class BaseAttribute(object):
    def __init__(self, **kwargs):
        super(BaseAttribute, self).__init__()
        self._attributes = {}
        self.attr(kwargs)

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
                for k, v in x[0].items():
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

    def clear_attributes(self):
        """Clear attributes of this instance then return self.
        """
        self._attributes.clear()
        return self

    def attribute_keys(self):
        """Return list of keys of attributes of this instance
        """
        return self._attributes.keys()

    def attribute_values(self):
        """Return list of values of attributes of this instance
        """
        return self._attributes.values()

    def attribute_items(self):
        """Return list of (key, value) of attributes of this instance
        """
        return util.cons_map(self._attributes.items(),
                             self._attributes.__class__,
                             dict)

    @property
    def attributes(self):
        """Return a copy of attributes of this instance
        """
        return self.attribute_items()

    @attributes.setter
    def attributes(self, x):
        """Set attributes of this instance to x. Return self.

        :param x: Mapping object
        """
        if not util.is_map(a):
            raise Exception('attribute must be a map')
        self._attributes = util.rec_decode(a)
        return self

    @attributes.deleter
    def attributes(self):
        """Clear current attributes. Return self.
        """
        self._attributes.clear()
        return self


class BaseProperty(object):
    def __init__(self, **kwargs):
        super(BaseProperty, self).__init__()
        self._properties = {}
        self.property(kwargs)

    def property(self, *x):
        """set/get properties.

        property('id'): Return value of 'id'

        property('id', 'a123'): set value of 'id' to 'a123' then return self

        :param x: single key, list, dict, set, tuple or key-value pair
        """
        if len(x) == 0:
            return self
        if len(x) == 1:
            if util.is_map(x[0]):
                for k, v in x[0].items():
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

    def clear_properties(self):
        """Clear properties of this instance then return self
        """
        self._properties.clear()
        return self

    def property_keys(self):
        """Return list of keys of properties of this instance
        """
        return self._properties.keys()

    def property_values(self):
        """Return list of values of properties of this instance
        """
        return self._properties.values()

    def property_items(self):
        """Return list of (key, value) of properties of this instance
        """
        return util.cons_map(self._properties.items(),
                             self._properties.__class__,
                             dict)

    @__builtin__.property
    def properties(self):
        """Return a copy of properties of this instance
        """
        return util.cons_map(self._properties.items(),
                             self._properties.__class__,
                             dict)

    @properties.setter
    def properties(self, x):
        """Set properties of this instance to x. Return self.

        :param x: Mapping object
        """
        if not util.is_map(a):
            raise Exception('property must be a map')
        self._properties = util.rec_decode(a)
        return self

    @properties.deleter
    def propeties(self):
        """Clear current properties. Return self.
        """
        self._properties.clear()
        return self
