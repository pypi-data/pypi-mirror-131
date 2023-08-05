__all__ = [
    'Person',
    'Patient',
    'Doctor',
    'Therapist',
    'Nurse',
    'Assistant',
    'Relative',
    'Employee',
    'BaseUser',
    'User',
]

from metadoctor import model
from metadoctor import field
from metadoctor import enumeration
from metadoctor import utils


class Person(model.BaseModel):
    fullname = field.Title(title='Nome Completo')
    gender = field.Choice(enumeration.Gender)
    birthdate = field.Date()
    
    
class Contact(model.BaseModel):
    phone1 = field.String()
    phone2 = field.String(required=False)
    email = field.String(required=False)
    
    
class Profession(model.BaseModel):
    graduation = field.Title(title='Área de Graduação')
    specialties = field.SemicolonStrToList(title='Especialidades', placeholder='separados por ponto e vírgular (;)', required=False)
    licence = field.String()
    
class Patient(Person, Contact):
    pass 

class Doctor(Person, Profession, Contact):
    pass 


class Nurse(Person, Profession, Contact):
    pass 


class Assistant(Person, Contact):
    pass 


class Employee(Person, Contact):
    pass 


class Relative(Person, Contact):
    pass 



class Therapist(Person, Profession, Contact):
    pass 