# -*- coding: utf-8 -*-
try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from importlib import import_module
import binascii
import json
import six


def get_module_attr(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
        return getattr(mod, attr, None)
    except ImportError:
        return None


__all__ = ('JSONField',)


# Utility functions to code/decode objects to/from JSON
def default_decode(cls_data_tuple):
    cls, data = cls_data_tuple
    cls = get_module_attr(cls)
    obj = cls.__new__(cls)
    obj.__dict__.update(data['__data__'])
    return obj


def encode_object(obj):
    if hasattr(obj, '__json__'):
        data = obj.__json__()
        if isinstance(data, tuple):
            decode, data = data
        else:
            decode = default_decode
            data = ('%s.%s' % (obj.__class__.__module__, obj.__class__.__name__), data)

        if callable(decode):
            decode = '%s.%s' % (decode.__module__, decode.__name__)

        return {
            '__decode__': decode,
            '__data__': data
        }
    else:
        data_string = binascii.b2a_base64(pickle.dumps(obj)).decode('utf-8')
        return dict(__pickled__=data_string)


def decode_object(d):
    if '__decode__' in d:
        return get_module_attr(d['__decode__'])(d['__data__'])
    elif '__pickled__' in d:
        ascii = d['__pickled__']
        return pickle.loads(binascii.a2b_base64(ascii.encode('utf-8')))
    else:
        return d


class JSONField(six.with_metaclass(models.SubfieldBase, models.TextField)):
    """JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly"""

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        if value == "":
            return None

        try:
            if isinstance(value, six.string_types):
                return json.loads(value, object_hook=decode_object)
        except ValueError:
            pass

        return value

    def get_prep_value(self, value):
        """Convert our JSON object to a string before we save"""
        if value == "" or value is None:
            return None

        value = json.dumps(value, default=encode_object, ensure_ascii=False, separators=(',',':'))

        return super(JSONField, self).get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.Field,
        }
        defaults.update(kwargs)
        defaults['widget'] = JSONTextarea
        return super(JSONField, self).formfield(**defaults)


class JSONTextarea(forms.Textarea):
    def value_from_datadict(self, data, files, name):
        value = data.get(name, '').strip()
        if value in ['', None]:
            return {}
        return json.loads(value)

    def render(self, name, value, attrs=None):
        return super(JSONTextarea, self).render(name, json.dumps(value), attrs=attrs)


class PickleField(six.with_metaclass(models.SubfieldBase, models.TextField)):
    """
    PickleField is a generic textfield that neatly serializes/unserializes
    any python objects seamlessly"""

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        if value == "":
            return None

        try:
            if isinstance(value, six.string_types):
                return pickle.loads(str(value))
        except ValueError:
            pass

        return value

    def get_prep_value(self, value):
        """Convert our JSON object to a string before we save"""
        if value == "" or value is None:
            return None

        value = pickle.dumps(value)
        return super(PickleField, self).get_prep_value(value)