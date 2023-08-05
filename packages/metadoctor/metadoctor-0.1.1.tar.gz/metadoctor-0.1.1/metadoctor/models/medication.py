__all__ = ['ActiveDrug']

from metadoctor import model
from metadoctor import field
from metadoctor import enumeration

class ActiveDrug(model.BaseModel):
    __project__ = 'default'
    __instance__ = 'active_drug'
    
    name = field.Title(title='Composto Ativo')
    
    
