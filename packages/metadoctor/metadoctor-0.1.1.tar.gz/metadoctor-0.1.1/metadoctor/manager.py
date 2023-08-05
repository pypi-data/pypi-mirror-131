#!/usr/bin/env python
# coding: utf-8
'''base_manager module'''

__all__ = ['BaseManager', 'PublicUser', 'AuthUser']

import asyncio
from abc import ABC
from functools import cache
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from metadoctor import db
from metadoctor import model
from metadoctor import enumeration


@dataclass 
class BaseUser(ABC):
    pass 


@dataclass 
class PublicUser(BaseUser):
    pass 


@dataclass 
class AuthUser(BaseUser):
    class Kind(Enum):
        P = 'Paciente' # patient 
        R = 'Familiar' # relative 
        D = 'Médico' # doctor 
        T = 'Terapeuta' # therapist 
        A = 'Assistente' # assistant 
        E = 'Funcionário' # employee 
        U = 'Indefinido' # undefined 
    username: str 
    picture: Optional[str] = None 
    name: Optional[str] = None 
    is_admin: bool = False 
    kind: Kind = field(default=Kind.U)
    
    
class BaseManager(ABC):
    __connection__ = db.Connection()
    
    def __init__(self, user: BaseUser =None) -> None:
        self.user = user or PublicUser()
        #self.user = BaseUser(settings.config.get('CURRENT_USER'))         
        
    @classmethod
    def conn(cls):
        return cls.__connection__
    
    @property
    def client(self):
        if isinstance(self.user, AuthUser):
            return self.conn().client
        return 
        
    
    @property
    def log(self):
        return self.conn().log
    
    @property
    def default(self):
        return self.conn().default
    
    
    @classmethod
    def db(cls, project: str = 'default'):
        return cls.conn().client if project in ['client'] else cls.conn().default if project in ['default'] else cls.conn().log

    
    @classmethod 
    def table(cls, instance: model.BaseModel):
        return instance.__table__ or type(instance).__name__
    
    @classmethod 
    def json(cls, instance: model.BaseModel):
        return instance.json
    
    @cache
    async def create_enum_db_all(self, table: str, project: str = 'default'):
        items = [(x.key, x) for x in await self.list_all(table, project)]
        return enumeration.BaseEnum(f'{model}Enum', items)
        
    @cache
    def sync_create_enum_db_all(self, table: str, project: str = 'default'):
        return asyncio.run(self.create_enum_db_all(table, project))
        
    @cache
    async def list_all(self, table: str, project: str = 'default') -> list:
        async with self.db(project).ListAll(table) as result:
            return [model(**item) for item in result]
        
    @cache
    def sync_list_all(self, table: str, project: str = 'default'):
        return asyncio.run(self.list_all(table, project))
    
    @cache
    async def check(self, instance: model.BaseModel, project: str = 'default'):
        db_all = await self.list_all(type(instance), project)
        return True if repr(instance) in [repr(x) for x in db_all] else False

    async def search(self, table: str, query: dict, project: str = 'default'):
        async with self.db(project).Search(table, query=query) as result:
            return [model(**item) for item in result]    

        
    def sync_search(self, table: str, query: dict, project: str = 'default'):
        return asyncio.run(self.search(table, query, project))
    
    async def save(self, instance: model.BaseModel, project: str = 'default'):
        base = self.conn().client if project == 'client' else self.conn().default if project == 'default' else self.conn().log
        async with base.Put(self.table(instance), self.json(instance)) as created:
            if created:
                return type(instance)(**created)
            return 
        
    def sync_save(self, instance: model.BaseModel, project: str = 'default'):
        return asyncio.run(self.save(instance=instance, project=project))
    
    async def get_or_create(self, instance: model.BaseModel, project: str = 'default'):
        async def search(self, instance: model.BaseModel, project: str = 'default'):
            async with self.db(project).Search(self.table(instance), instance.__json_main__()) as result:
                if result:
                    return [type(instance)(**item) for item in result]
                return []
        exist = await search(instance, project)
        if len(exist) == 0:
            return await self.save(instance, project)
        return exist[0]


    def sync_get_or_create(self, instance: model.BaseModel, project: str = 'default'):
        return asyncio.run(self.get_or_create(instance=instance, project=project))
    
    @cache
    def get_form(self, model: model.BaseModel, method='get', action="."):
        result = f'<form id="{model.__name__}Form" class="model-form" method="{method}" action="{action}" novalidate>'
        for field in model.fields().values():
            result += field.get_form_field()
        result += '<hr><input type="submit"><hr>'
        result += '</form>'
        return result 
    
