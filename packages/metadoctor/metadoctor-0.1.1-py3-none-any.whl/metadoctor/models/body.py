__all__ = ['Organ', 'Cid10']

from metadoctor import model
from metadoctor import field
from metadoctor import enumeration

class Organ(model.BaseModel):
    __project__ = 'default'
    __instance__ = 'organ'
    
    name = field.Title(title='Nome do Órgão')
    system = field.Choice(enumeration.BodySystem, title='Sistema')
    
    
class Cid10(model.BaseModel):
    __project__ = 'default'
    __instance__ = 'cid10'
    
    code = field.String()
    title = field.String(exclude=True)