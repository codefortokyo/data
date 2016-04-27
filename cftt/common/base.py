# -*- coding: utf-8 -*-

import collections
import __builtin__
import copy

import util


class _DecodedDict(collections.MutableMapping):
    """DecodedDict is an child class of collections.MutableMapping.
    Each element is decoded to unicode if possible.
    """
    def __init__(self, *arg, **kwargs):
        super(_DecodedDict, self).__init__()
        self._elements = dict()
        self(dict(*arg, **kwargs))

    def _get(self, single_key):
        if single_key in self._elements:
            return copy.deepcopy(self._elements[single_key])
        return None

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
        return self._get(k)

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

    def __contains__(self, x):
        if util.is_map(x):
            return all((self.__contains__(v) for v in x.values()))
        if util.is_array(x):
            return all((self.__contains__(v) for v in x))
        if util.is_string(x):
            k = util.safe_decode(x)
        else:
            k = unicode(x)
        return k in self._elements

    def __str__(self):
        return self._elements.__str__()

    def __eq__(self, other):
        return self._elements.__eq__(_DecodedDict(other)._elements)

    def __ne__(self, other):
        return not self._elements.__eq__(_DecodedDict(other)._elements)

    def get(self, key, default=None):
        if self.__contains__(key):
            return self.__getitem__(key)
        return default

    def pop(self, key, default=None):
        if self.__contains__(key):
            ret = self.__getitem__(key)
            self.__delitem__(key)
            return ret
        return default

    def setdefault(self, key, default=None):
        if self.__contains__(key):
            return self[key]
        self[key] = default
        return self[key]

    def dump(self, encoding=None):
        if encoding is not None:
            return util.rec_encode(dict(self.items()), encoding)
        return dict(self.items())


class BaseAttribute(object):
    """designed for object with attribute
    """
    def __init__(self, *x, **kwargs):
        super(BaseAttribute, self).__init__()
        self._attributes = _DecodedDict(*x, **kwargs)

    def attr(self, *x):
        """set/get attributes.

        attr('id'): Return value of 'id'

        attr('id', 'a123'): set value of 'id' to 'a123' then return self

        :param x: single key, list, dict, set, tuple or key-value pair
        """
        ret = self._attributes(*x)
        if ret is self._attributes:
            return self
        return ret

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
        return self._attributes.items()

    @property
    def attributes(self):
        """Return  attributes of this instance
        """
        return self._attributes

    @attributes.setter
    def attributes(self, x):
        """Set attributes of this instance to x. Return self.

        :param x: Mapping object
        """
        self._attributes = _DecodedDict(x)
        return self

    @attributes.deleter
    def attributes(self):
        """Clear current attributes. Return self.
        """
        self._attributes.clear()
        return self


class BaseProperty(object):
    """designed for object with property
    """
    def __init__(self, *x, **kwargs):
        super(BaseProperty, self).__init__()
        self._properties = _DecodedDict(*x, **kwargs)

    def property(self, *x):
        """set/get properties.

        property('id'): Return value of 'id'

        property('id', 'a123'): set value of 'id' to 'a123' then return self

        :param x: single key, list, dict, set, tuple or key-value pair
        """
        ret = self._properties(*x)
        if ret is self._properties:
            return self
        return ret

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
        return self._properties.items()

    @__builtin__.property
    def properties(self):
        """Return properties of this instance
        """
        return self._properties

    @properties.setter
    def properties(self, x):
        """Set properties of this instance to x. Return self.

        :param x: Mapping object
        """
        self._properties = _DecodedDict(x)
        return self

    @properties.deleter
    def properties(self):
        """Clear current properties. Return self.
        """
        self._properties.clear()
        return self


class Stream(BaseAttribute, collections.Iterable):
    def __init__(self, upstream, generate, attr=None):
        super(Stream, self).__init__(attr or {})
        self._upstream = upstream
        self._generate = generate

    def __iter__(self):
        return self._generate(self, self._upstream)


class BasePipe(object):
    __default_event_handler = {
        'initialize': None,
        'finalize': None,
        'iterate': None,
        'error': lambda s, e: util._raise(e)
    }

    @classmethod
    def set_default_event_handler(cls, event_name, event_handler):
        if event_name in cls.__default_event_handler:
            cls.__default_event_handler[event_name] = event_handler

    def __init__(self):
        super(BasePipe, self).__init__()
        self.__event_handler = {}

    def __call__(self, upstream):
        if isinstance(upstream, BaseAttribute):
            return Stream(upstream=upstream, generate=self.__generate(),
                          attr=upstream.attributes)
        return Stream(upstream=upstream,
                      generate=self.__generate())

    def __get_event_handler(self, event_name):
        if event_name in self.__event_handler:
            return self.__event_handler[event_name]
        return self.__class__.__default_event_handler[event_name]

    def on(self, event_name, event_handler):
        if event_name in self.__class__.__default_event_handler:
            if event_handler is None:
                del self.__event_handler[event_name]
            else:
                self.__event_handler[event_name] = event_handler

    def _initialize(self):
        """default behavior. should be overwritten.
        """
        return lambda s, u: u

    def _finalize(self):
        """default behavior. should be overwritten.
        """
        return lambda s: s

    def _iterate(self):
        raise Exception('_iterate not implemented')
        # return lambda s, x: x

    def __initialize(self):
        eh = self.__get_event_handler('initialize')
        if eh is None:
            return self._initialize()

        def f(stream, upstream):
            ret = self._initialize()(stream, upstream)
            eh(stream, ret)
            return ret
        return f

    def __finalize(self):
        eh = self.__get_event_handler('finalize')
        if eh is None:
            return self._finalize()

        def f(stream, upstream):
            ret = self._finalize()(stream)
            eh(stream, ret)
            return ret
        return f

    def __iterate(self):
        return self._iterate()

    def __generate(self):
        initialize = self.__initialize()
        finalize = self.__finalize()
        iterate = self.__iterate()
        error = self.__get_event_handler('error')
        if self.__get_event_handler('iterate') is not None:
            on_iterate = self.__get_event_handler('iterate')

            def f(stream, upstream):
                try:
                    for x in initialize(stream, upstream):
                        y = iterate(stream, x)
                        if y is not None:
                            yield y
                            on_iterate(stream, y)
                    finalize(stream, upstream)
                except StopIteration:
                    raise StopIteration
                except Exception as e:
                    error(stream, e)
                finally:
                    raise StopIteration
            return f
        else:
            def f(stream, upstream):
                try:
                    for x in initialize(stream, upstream):
                        y = iterate(stream, x)
                        if y is not None:
                            yield y
                    finalize(stream, upstream)
                except StopIteration:
                    raise StopIteration
                except Exception as e:
                    error(stream, e)
                finally:
                    raise StopIteration
            return f
