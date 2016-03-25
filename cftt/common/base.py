# -*- coding: utf-8 -*-

import collections

import util


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
        return util.cons_map(self._attributes.items(),
                             self._attributes.__class__,
                             dict)

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

    @property
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
