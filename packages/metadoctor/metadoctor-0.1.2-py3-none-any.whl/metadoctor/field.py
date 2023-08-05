#!/usr/bin/env python
# coding: utf-8
'''BaseField Module'''

__all__ = [
    'BaseField',
    'RegularField',
    'EnumField', 
    'ReferenceField', 
    'DateTime', 
    'Text', 
    'SemicolonStrToList',
    'String', 
    'Choice',
    'Date',
    'Title',
    'Number', 
    'Integer',
    'Float',
    'Real', 
    'Key',
    'KeyData'
    ]

import re
import datetime
from abc import ABC
from collections import ChainMap
from decimal import Decimal
from typing import Any

from metadoctor import enumeration
from metadoctor import db

POSITIONAL_HTML_ELEMENT_ATTRIBUTES = 'required hidden disabled multiple readonly'.split()
KEYWORD_VALUE_HTML_ELEMENT_ATTRIBUTES = 'placeholder value max min minlength maxlength step pattern type'.split()
BASE_FIELD_CONFIG_KEYS = 'transform fsize fclass tag default factory exclude title description options'.split()

class BaseField(ABC):
    __positional__ = POSITIONAL_HTML_ELEMENT_ATTRIBUTES
    __keyvalue__ = KEYWORD_VALUE_HTML_ELEMENT_ATTRIBUTES
    __config__ = [*BASE_FIELD_CONFIG_KEYS, *POSITIONAL_HTML_ELEMENT_ATTRIBUTES, *KEYWORD_VALUE_HTML_ELEMENT_ATTRIBUTES]
    __config_defaults__ = dict(required=True, fsize=(12,6,3), tag='input', type='text')
    
    def __init__(self, *args, **kwargs) -> None:
        
        if len(args) > 0:
            if type(args[0]) == str:
                self.owner = None
                self.owner_name = args[0]
            else:
                self.owner = args[0]
                self.owner_name = self.owner.__name__
        else:
            self.owner = enumeration.Variable.UNDEFINED
            self.owner_name = enumeration.Variable.UNDEFINED
    
        for key, val in kwargs.items():
            if key in self.__config__:
                setattr(self, key, val)
        for key in self.__config__:
            if not hasattr(self, key):
                if key in self.__config_defaults__.keys():
                    setattr(self, key, self.__config_defaults__[key])
                else:
                    setattr(self, key, enumeration.Variable.UNDEFINED)

    def get_form_attrs(self) -> str:
        result = ''
        for k,v in vars(self).items():
            if enumeration.Variable.is_defined(v):
                if k in self.__keyvalue__:
                    result += f' {k}="{v}"'
                elif k in self.__positional__ and v == True:
                    result += f' {k}'
        if hasattr(self, '_pre_defined_value_'):
            result += f' value={self._pre_defined_value_}'
        print(result)
        return ' '.join([x for x in re.split('\s', result)])
    
    def get_form_field(self) -> str:
        content = self.options if self.tag in ['select'] else ''
        label_content = self.title if enumeration.Variable.is_defined(self.title) else self.public_name
        helper_content = self.description if enumeration.Variable.is_defined(self.description) else ''
        cols = 'col-sm-{} col-md-{} col-lg-{}'.format(*self.fsize)
        label = lambda content: f'<label class="form-label">{content}</label>'
        span = lambda content: f'<span class="form-helper">{content}</span>'
        div = lambda content: f'<div class="form-field-container {cols}">{content}</div>'
        return div(label(label_content) + f'<{self.tag} {self.get_form_attrs()}>{content}</{self.tag}>'.replace('</input>', '') + span(helper_content))
        
        
    def __set_name__(self, obj, name) -> None:
        self.public_name = name 
        self.private_name = f'_{name}'

    def pre_validation(self, obj, value) -> Any:
        if not enumeration.Variable.exist(value):
            if enumeration.Variable.is_defined(self.factory):
                value = self.factory()
                setattr(self, '_pre_defined_value_', value)
            elif enumeration.Variable.is_defined(self.default):
                value = self.default        
                setattr(self, '_pre_defined_value_', value)
            else:
                setattr(self, '_pre_defined_value_', None)
        else:
            setattr(self, '_pre_defined_value_', None)
        return value
    
    def check_required(self, obj, value) -> None:
        if self.required == True:
            if not enumeration.Variable.exist(value):
                raise ValueError(f'{type(obj).__name__}.{self.public_name} cannot be "{value}"')
            
    def post_validation(self, obj, value) -> Any:
        if enumeration.Variable.exist(value):
            if enumeration.Variable.is_defined(self.transform):
                if not issubclass(type(self), (EnumField, ReferenceField)):
                    return self.transform(value)
        return value
            
            
    def validate(self, obj, value) -> None:
        self.check_required(obj, value)
        if enumeration.Variable.exist(value):
            if enumeration.Variable.is_defined(self.min):
                if float(self.min) > value:    
                    raise ValueError(f'{self._name_} of {type(obj).__name__} is "{value}" and cannot be lesser then {self.min}')
            if enumeration.Variable.is_defined(self.max):
                if float(self.max) < value:    
                    raise ValueError(f'{self._name_} of {type(obj).__name__} is "{value}" and cannot be greater then {self.max}')
            if enumeration.Variable.is_defined(self.minlength):
                if float(self.minlength) > len(value):    
                    raise ValueError(f'{self._name_} of {type(obj).__name__} is "{value}" and cannot has length lesser then {self.minlength}')
            if enumeration.Variable.is_defined(self.maxlength):
                if float(self.maxlength) < value:    
                    raise ValueError(f'{self._name_} of {type(obj).__name__} is "{value}" and cannot be greater then {self.maxlength}')
            if enumeration.Variable.is_defined(self.pattern):
                if not re.match(self.pattern, value):
                    raise ValueError(f'{self._name_} of {type(obj).__name__} is "{value}" does not match {self.pattern}')
                    
    def __set__(self, obj, value) -> None:
        pre = self.pre_validation(obj, value)
        self.validate(obj, pre)
        post = self.post_validation(obj, pre)
        setattr(obj, self.private_name, post)
        
    def parse(self, obj, value) -> Any:
        return value 
    
    def __get__(self, obj, owner=None) -> Any:
        value = getattr(obj, self.private_name)
        return self.parse(obj, value)
    

class  RegularField(BaseField):
    pass 


class  EnumField(BaseField):
    pass 

        
class ReferenceField(BaseField):
    pass 


class DateTime(RegularField):
    def __init__(self, **kwargs) -> None:
        super().__init__(datetime.datetime, **kwargs) 
        self.tag = 'input'
        self.type = 'datetime-local'
        
        
class Text(RegularField):
    def __init__(self, **kwargs) -> None:
        super().__init__(str, **kwargs) 
        self.tag = 'textarea'
        self.type = enumeration.Variable.UNDEFINED

        
class SemicolonStrToList(RegularField):
    def __init__(self, **kwargs) -> None:
        super().__init__(str, **kwargs) 
        self.tag = 'textarea'
        self.type = enumeration.Variable.UNDEFINED

    
    def parse(self, obj, value):
        trim = lambda x: x.strip()
        split = lambda x: x.split(";")
        process = lambda x: [i for i in sorted([trim(w) for w in split(x) if w not in ['', None]]) if i not in ['', None]]
        if value:
            return process(value)
        return value

    
class String(RegularField):
    def __init__(self,**kwargs) -> None:
        super().__init__(str, **kwargs) 


    def parse(self, obj, value):
        return value

        
class Choice(EnumField):
    '''
    Receive enumeration name to store in db. 
    The __get__ method return the enumeration member instance.
    '''
    
    def __init__(self,enum, **kwargs) -> None:
        super().__init__(enum, **kwargs) 
        self.tag = "select"
        self.type = enumeration.Variable.UNDEFINED
        self.options = ''.join([f'<option value="{key}">{value}</option>' for key, value in self.owner.choices()])

        
    def  parse(self, obj, value):
        if value:
            return {e.name: e.name for e in self.owner.__members__.values()}[value]
        return value 
    
    
class Date(RegularField):
    '''
    Receive date as a isoformat string to store in db. 
    The __get__ method return the datetime.date instance.
    '''
    
    def __init__(self, **kwargs) -> None:
        super().__init__(datetime.date, **kwargs) 
        self.tag = 'input'
        self.type = 'date'


    def  parse(self, obj, value):
        return datetime.date.fromisoformat(value) if isinstance(value, str) else value  


class Title(RegularField):
    '''
    Receive a string to store in db formated to title().
    The __get__ method return the string.
    '''
    
    def __init__(self, **kwargs) -> None:
        super().__init__(str, **kwargs) 

    def parse(self, obj, value):
        if isinstance(value, str):
            return value.title()
        return value 

    
class Number(RegularField):
    def __init__(self, **kwargs) -> None:
        super().__init__(float, **kwargs) 
        self.tag = 'input'
        self.type = 'number'

    def parse(self, obj, value):
        return float(value) if isinstance(value, str) else value  

    
class Integer(RegularField):
    def __init__(self,**kwargs) -> None:
        super().__init__(int, **kwargs) 
        self.tag = 'input'
        self.type = 'number'
        
    def parse(self, obj, value):
        return int(value) if isinstance(value, str) else value  

    
class Float(RegularField):
    def __init__(self, **kwargs) -> None:
        super().__init__(float, **kwargs) 
        self.tag = 'input'
        self.type = 'number'
        
    def parse(self, obj, value):
        return float(value) if isinstance(value, str) else value  

    
class Real(RegularField):
    def __init__(self,**kwargs) -> None:
        super().__init__(Decimal, **kwargs) 
        self.tag = 'input'
        self.type = 'number'
                
    def parse(self, obj, value):
        if value:
            return Decimal(value)
        return value


class KeyData(ReferenceField):
    def __init__(self,table, project='client', fields=None, **kwargs) -> None:
        super().__init__(table, **kwargs) 
        self.project = project
        self.tag = 'select'
        self.type = enumeration.Variable.UNDEFINED
        self.table = self.owner_name
        self.fields = fields or list()
        
    def parse(self, obj, value):
        base = db.ClientDB()
        conn = base.sync_connect(self.table)
        dbdata = conn.get(value)
        result = ChainMap({}, *[x for x in dbdata.values() if isinstance(x, dict)])
        fields = self.attrs if isinstance(self.fields, list) else self.fields.split()
        result.update({"key": value, "table": self.table})
        for item in fields:
            result.update({item: result.get(item)})
        return result.maps[0]
    

class Key(ReferenceField):
    def __init__(self,table, project='Client', **kwargs) -> None:
        super().__init__(table, **kwargs) 
        self.project = project
        self.tag = 'select'
        self.type = enumeration.Variable.UNDEFINED
        self.table = self.owner_name