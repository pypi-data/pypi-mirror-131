#!/usr/bin/env python
# coding: utf-8
'''base_model module'''

__all__ = ['BaseModel']


from abc import ABC
from collections import ChainMap
from markupsafe import Markup

from metadoctor import field
from metadoctor import db
from metadoctor import enumeration
from metadoctor import utils


class BaseModel(ABC):
    __project__ = 'default'
    __instance__ = None
    __table__ = None
    __singular__ = None
    __plural__ = None
    
    def __init__(self, *args, key=None, **kwargs) -> None:
        self._args_ = args 
        self._kwargs_ = kwargs
        self._key = key 
        for base in reversed(type(self).__bases__):
            if issubclass(base, BaseModel):
                for k, field in base.fields().items():
                    setattr(type(self), k, field) 
        for k in self.fields().keys():
            if k in self._kwargs_.keys():
                setattr(self, k, kwargs[k])
            else:
                setattr(self, k, None)
                
    @classmethod
    def table(cls):
        return cls.__table__ or cls.__name__
            
    @property
    def key(self):
        return getattr(self, '_key')
    
    @classmethod
    def __regular_fields__(cls):
        return {k:v for (k,v) in cls.fields().items() if isinstance(v, field.RegularField)}
    
    @classmethod
    def __reference_fields__(cls):
        return {k:v for (k,v) in cls.fields().items() if isinstance(v, field.ReferenceField)}
    
    @classmethod
    def __enum_fields__(cls):
        return {k:v for (k,v) in cls.fields().items() if isinstance(v, field.EnumField)}
    
    @classmethod
    def fields(cls):
        return {k:v for (k,v) in vars(cls).items() if isinstance(v, field.BaseField)}
    
    @classmethod
    async def list_all(cls):
        base: db.ClientDB()
        db_objects = []
        async with base.ListAll(cls.__table__ or cls.__name__) as result:
            for item in result:
                data = ChainMap({}, item)
                for k in cls.fields().keys():
                    data.update({k: data.get(k)})    
                db_objects.append(cls(**data))
        return db_objects      
    
    @classmethod
    async def get_one(cls, key: str):
        base = db.ClientDB()
        async with base.Get(cls.__table__ or cls.__name__, key) as result:
            if result:
                data = ChainMap({}, result)
                for k in cls.fields().keys():
                    data.update({k: data.get(k)})    
                return cls(**data)
            return  

    async def get_self(self):
        base = db.ClientDB()
        async with base.Get(type(self).__name__, self.key) as result:
            if result:
                data = ChainMap({}, result)
                for k in self.fields().keys():
                    data.update({k: data.get(k)})    
                return type(self)(**data)
            return 
        
    def __str__(self) -> str:
        return ', '.join([str(v.__get__(self)) for v in self.fields().values() if enumeration.Variable.exist(v.__get__(self))])
    
    
    def __main_fields__(self) -> str:
        return {k:v for k, v in self.fields().items() if not enumeration.Variable.is_defined(v.exclude)}
                
    def __repr__(self) -> str:
        return f'{type(self).__name__}({", ".join([f"{k}={str(v.__get__(self))}" for k, v in self.__main_fields__().items()])}' 

    def __str_html__(self) -> str:
        return Markup(f'<h3>{str(self)}</h3>')
    
    def __json__(self) -> dict:
        return {k: utils.json_encode(v) for k,v in self.data.items()}
    
    def __json_main__(self) -> dict:
        return {k: utils.json_encode(v.__get__(self)) for k,v in self.__main_fields__().items()}
    
    def __data__(self) -> dict:
        result = {k:v.__get__(self) for (k,v) in vars(type(self)).items() if not k.startswith('_') and not k.endswith('_')}
        if self.key:
            result['key'] = self.key
        return result 
    
    def __extra_fields__(self):
        extra_fields = dict()
        for k,v in self._kwargs_.items():
            if not k in self.fields().keys():
                extra_fields.update({k:v}) 
        return extra_fields
        
    @property
    def json(self) -> dict:
        return self.__json__()
    
    @property
    def data(self) -> dict:
        return self.__data__()

    @property
    def defaults(self) -> dict:
        defaults = {}
        for k,v in self.fields().items():
            if enumeration.Variable.is_defined(v.factory):
                defaults.update({k: v.factory()})  
            elif enumeration.Variable.is_defined(v.default):
                defaults.update({k: v.default})
        return defaults