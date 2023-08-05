__all__ = ['Service']

from metadoctor import model
from metadoctor import field
from metadoctor import enumeration

class Service(model.BaseModel):
    __project__ = 'default'
    __instance__ = 'service'
    
    name = field.Title()
    type = field.Choice(enumeration.VisitType)
    revisit = field.Choice(enumeration.Permission)