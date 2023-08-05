#!/usr/bin/env python
# coding: utf-8

"""Utils module"""

__all__ = [
    'json_encode',
    'is_private',
    'unprivate',
    'remove_accents',
    'today',
    'normalize',
    'age',
    'today',
    'now'
    ]

from enum import Enum 
from datetime import timedelta, date, datetime
from decimal import Decimal
import unicodedata 
from typing import Union

today = date.today
now = datetime.now
normalize = lambda string: unicodedata.normalize('NFKD', string)

def age(birthdate: Union[date, str]) -> int:
    return ((today() - birthdate if isinstance(birthdate, date) else date.fromisoformat(birthdate)).days/365).__round__(2)

def remove_accents(string: str) -> str:
    return ''.join([c for c in normalize(string) if not unicodedata.combining(c)])

def is_private(string: str) -> bool:
    return True if string.startswith("_") and not string.endswith("_") else False

def unprivate(string: str) -> str:
    return string[ 1: ] if is_private(string) else string

def json_encode(value):
    if value == None:
        return ''
    elif isinstance(value, bool):
        return 'true' if value == True else 'false'
    elif isinstance(value, (str, int, float)):
        return value
    elif isinstance(value, Decimal):
        return str(value)
    elif isinstance(value, list):
        return [json_encode(i) for i in value]
    elif isinstance(value, dict):
        return {unprivate(k): json_encode(v) for k, v in value.items()}
    elif isinstance(value, Enum):
        return str(value)
    elif isinstance(value, (datetime, date)):
        return value.isoformat()
    elif isinstance(value, timedelta):
        return f'{value.days} {"dias"  if value.days > 1 else "dia"}'
    elif isinstance(value, tuple):
        try:
            return {k: json_encode(v) for (k,v) in value._asdict().items()}
        except:
            return [json_encode(v) for v in value]
    else:
        return str(value)
        