#!/usr/bin/env python
# coding: utf-8

from abc import ABC 
from enum import Enum
import html as pyhtml 
from dataclasses import dataclass, field
from typing import Optional, Union, Any, List, Dict, Tuple, TypeVar


class BaseEnum(Enum):
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f'{type(self).__name__}.{self.name}'
    
    @classmethod
    def members(cls):
        return [m for m in cls.__members__.values()]
    

class TOF(BaseEnum):
    TRUE = 'true'
    FALSE = 'false'
    
    
class YON(BaseEnum):
    YES = 'yes'
    NO = 'no'
    

class InputType(BaseEnum):
    TEXT='text'
    DATETIME_LOCAL='datetime-local'
    DATE='date'
    SUBMIT='submit'
    NUMBER='number'
    WEEK='week'
    COLOR='color'
    IMAGE='image'
    MONTH='month'
    RANGE='range'
    BUTTON="button"
    CHECKBOX="checkbox"
    EMAIL="email"
    FILE="file"
    HIDDEN="hidden"
    PASSWORD="password"
    RADIO="radio"
    RESET="reset"
    SEARCH="search"
    TEL="tel"
    TIME="time"
    URL="url"
    
    def __str__(self):
        return f'type="{self.value}"'
    
    
@dataclass 
class BaseElement(ABC):
    tag: str 
    pk: Optional[str] = None
    klass: Optional[str] = None
    style: Optional[str] = None
    title: Optional[str] = None
    accesskey: Optional[str] = None
    lang: Optional[str] = None
    hidden: Optional[bool] = None
    tabindex: Optional[int] = None
    contenteditable: Optional[TOF] = None
    spellcheck: Optional[TOF] = None
    draggable: Optional[TOF] = None
    translate: Optional[YON] = None
    data_attr: Optional[Tuple[str, str]] = None
    content: List[Union[str, 'BaseElement', None]] = field(default_factory=list)
    is_empty: bool = False 
    has_items: bool = False 
    has_options: bool = False 

    @property
    def _tag(self):
        return self.tag.lower()
    
    @property
    def _pk(self):
        return f'id="{self.pk}"' if self.pk else None 
    
    @property
    def _data_attr(self):
        return f'data-{self.data_attr[0]}="{self.data_attr[1]}"' if self.data_attr else None
                         
    @property        
    def _klass(self):
        return f'class="{self.klass}"' if self.klass else None 
            
    @property        
    def _style(self):
        return f'style="{self.style}"' if self.style else None 
                         
    @property        
    def _title(self):
        return f'title="{self.title}"' if self.title else None  
                         
    @property        
    def _accesskey(self):
        return f'accesskey="{self.accesskey}"' if self.accesskey else None 

    @property        
    def _tabindex(self):
        return f'tabindex="{self.tabindex}"' if self.tabindex else None 
                         
    @property        
    def _lang(self):
        return f'lang="{self.lang}"' if self.lang else None 
                         
    @property        
    def _hidden(self):
        return 'hidden' if self.hidden == True else None 
                                    
    @property        
    def _contenteditable(self):
        return f'contenteditable="{self.contenteditable}"' if self.contenteditable else None 
    
    @classmethod
    def parse_item(cls, item):
        return f'<li>{item}</li>'
    
    @classmethod
    def parse_option(cls, value, option):
        return f'<option value="{value}">{option}</option>'
    
    @property        
    def _content(self):
        if self.is_empty:
            return ''
        else:
            result = []
            if self.has_items:
                for item in self.content:
                    result.append(self.parse_item(str(item)))
            elif self.has_options:
                for item in self.content:
                    result.append(self.parse_option(*item if isinstance(item, (tuple, list)) else (item, item) if isinstance(item, str) else (item.name, item.value) if isinstance(item, Enum) else (str(item), str(item))))
            else:
                for item in self.content:
                    result.append(str(item))   
            return ''.join(result)
                         
    def _global_attributes_str(self) -> str:
        return ' '.join(filter(lambda x: x != None, [self._pk, self._klass, self._style, self._title, self._accesskey, self._tabindex, self._lang, self._hidden, self._contenteditable]))
    
    def _local_attributes_str(self) -> str:
        return '' 

    def _attributes(self) -> str:
        return ' '.join([x for x in [self._global_attributes_str(), self._local_attributes_str()] if len(x) > 0])
        
    def _repr_html_(self):
        if self.is_empty:
            return f'<{" ".join([self._tag, self._attributes()])}>'
        return f'<{" ".join([self._tag, self._attributes()])}>{self._content}</{self._tag}>'
    
    def __str__(self):
        return self._repr_html_()  
    
    
@dataclass 
class Element(BaseElement):
    pass 


@dataclass 
class Fieldset(Element):
    legend: Optional[str] = None
    
    @property
    def _content(self) -> str:
        content = [str(self.legend)]
        if self.content:
            if isinstance(self.content, list):
                content = [self.legend, *self.content]
            elif isinstance(self.content, str):
                content = [self.legend, self.content]
        return ''.join(content)

@dataclass 
class Ol(Element):
    tag: str = 'OL'
    has_items: bool = True
    
@dataclass 
class Ul(Element):
    tag: str = 'UL'
    has_items: bool = True

@dataclass 
class Select(Element):
    tag: str = 'SELECT'
    has_options: bool = True
    
    
@dataclass 
class TextArea(Element):
    tag: str = 'TEXTAREA'
    
@dataclass 
class Div(Element):
    tag: str = 'DIV'
    
@dataclass 
class Input(Element):
    tag: str = 'INPUT'
    input_type: Optional[InputType] = None
    is_empty: str = True
    label: Optional[str] = None
    
    def _local_attributes_str(self):
        return str(InputType('text')) if not self.input_type else str(self.input_type)
    
    @property 
    def _content(self):
        if self.label:
            content = [str(self.label)]
            if self.content:
                if isinstance(self.content, list):
                    content = content.extend(self.content)
                elif isinstance(self.content, str):
                    content = content.append(self.content)
            if self.inline:
                return ': '.join(content)
        return ':<br>'.join(content)
            

    
FormField = Union[Input, Select, TextArea]


@dataclass 
class Label(Element):
    tag: str = 'LABEL'
    form_field: FormField = field(default=...)
    inline: bool = True
    
    def _local_attributes_str(self):
        return f'for="{self.form_field._pk}"'
    
    @property
    def _content(self) -> str:
        content = [str(self.form_field)]
        if self.content:
            if isinstance(self.content, list):
                content = [*self.content, str(self.form_field)]
            elif isinstance(self.content, str):
                content = [self.content, str(self.form_field)]
        if self.inline:
            return ': '.join(content)
        return ':<br>'.join(content)
