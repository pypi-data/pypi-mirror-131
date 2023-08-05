#!/usr/bin/env python
# coding: utf-8

"""BaseEnum module"""

__all__ = [
    'Cid10',
    'Variable',
    'BaseEnum',
    'StrEnum', 
    'TupleEnum', 
    'Day', 
    'Frequency', 
    'Month', 
    'Permission',
    'Right',
    'Access',
    'Gender',
    'VisitType',
    'ActiveDrugType',
    'Pharmaceutical',
    'RecipeType',
    'DosageUnit',
    'DosageForm',
    'DosageUse',
    'ActiveDrug',
    'Brand',
    'Drug',
    'Experience',
    'BodySystem',
    'today',
    'now'
    ]

from enum import Enum 
import csv 
from datetime import timedelta, date, datetime
from typing import Union
from collections import ChainMap
from functools import cache

from metadoctor import utils
from metadoctor import settings

today = date.today
now = datetime.now()

class Variable(Enum):
    UNDEFINED = '<undefined>'
    MISSING = '<missing>'
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value

    @staticmethod
    def is_defined(value):
        return False if value == Variable.UNDEFINED else True
    
    @staticmethod
    def is_missing(value):
        return True if value == Variable.MISSING else False
    
    @staticmethod
    def exist(value):
        return False if value in ['', None, Variable.MISSING, Variable.UNDEFINED] else True

class BaseEnum(Enum):
    
    def __str__(self) -> str:
        if type(self.value) == str:
            return self.value
        elif type(self.value) == int:
            return str(self.value)
        elif type(self.value) == tuple:
            if len(self.value) == 1:
                return str(self.value[0])
            else:
                return str(self.value[1])
        else:
            return str(self.value)
    
    def __repr__(self) -> str:
        return f'{type(self).__name__}.{self.name}'
    
    @classmethod
    @cache
    def choices(cls):
        '''member name as keyword and str of member as value'''
        return [(e.name, str(e)) for e in cls.__members__.values()]

    @classmethod
    @cache
    def name2member_map(cls):
        '''member name as keyword and member as value'''
        return {e.name: e for e in cls.__members__.values()}
    
    @classmethod
    @cache
    def str2member_map(cls):
        '''normalized and lower str of member as keyword and member as value'''
        return {utils.remove_accents(str(e)).lower(): e for e in cls.__members__.values()}
    
    
    @classmethod
    @cache
    def int2member_map(cls):
        '''int as keyword and member as value'''
        try:
            return {int(e): e for e in cls.__members__.values()}
        except:
            return {}
    
    @classmethod
    @cache
    def value2member_map(cls):
        '''member value as keyword and member as value'''
        return {e.value: e for e in cls.__members__.values()}
    
    @classmethod
    @cache
    def get(cls, v: Union[str, int]):
        return ChainMap(
            cls.name2member_map(), 
            cls.str2member_map(), 
            cls.value2member_map(), 
            cls.int2member_map()
        ).get(utils.remove_accents(v).lower() if isinstance(v, str) else v)


class StrEnum(str, BaseEnum):
    '''
    StrEnum
    '''

    
class TupleEnum(tuple, BaseEnum):
    '''
    TupleEnum
    `````````
    '''

    def __str__(self) -> str:
        return str(self.value[1])
    
    def __int__(self) -> int:
        return self.value[0]


class Day(timedelta, BaseEnum):
    '''
    Day enumerator 
    '''
    _ignore_ = 'Day item'
    Day = vars()
    for item in range(366):
        Day[f'{item}'] = item
        
    def __str__(self) -> str:
        days = self.value.days
        return f'{days} {"dia" if days <= 1 else "dias"}'
    
    @classmethod
    def __date_ahead__(cls, v: int):
        return today() + cls[str(v)].value
    
    @classmethod
    def __date_ago__(cls, v: int):
        return today() - cls[str(v)].value
    
    @classmethod
    def value2member_map(cls):
        members = cls.__members__.values()
        return {**{e.value.days: e for e in members}, **{e.value: e for e in members}}


class Month(TupleEnum):
    JAN = 1, "January", "Janeiro", "Jan"
    FEB = 2, "February", "Fevereiro", "Fev"
    MAR = 3, "March", "Março", "Mar"
    APR = 4, "April", "Abril", "Abr"
    MAY = 5, "May", "Maio", "Mai"
    JUN = 6, "June", "Junho", "Jun"
    JUL = 7, "July", "Julho", "Jul"
    AUG = 8, "August", "Agosto", "Ago"
    SEP = 9, "September", "Setembro", "Set"
    OCT = 10, "October", "Outubro", "Out"
    NOV = 11, "November", "Novembro", "Nov"
    DEZ = 12, "December", "Dezembro", "Dez"
    
    def __int__(self):
        return self.value[0]

    def __str__(self):
        return self.value[2]
    
    def __tuple__(self):
        return self.value


class Frequency(TupleEnum):
    '''
        Frequency Enum 
            tuple type enumeration
            properties: title display hours 
    '''
    NO = 'Nenhuma', 'nenhuma', 0, False
    QAM = 'Manhã', 'pela manhã', 24, True
    QPM = 'Tarde', 'à tarde', 24, True
    QHS = 'Noite', 'à noite', 24, True
    Q1H = '1/1h', 'a cada 1 horas', 1, True
    Q2H = '2/2h', 'a cada 2 horas', 2, True
    Q3H = '3/3h', 'a cada 3 horas', 3, True
    Q4H = '4/4h', 'a cada 4 horas', 4, True
    Q6H = '6/6h', 'a cada 6 horas', 6, True
    Q8H = '8/8h', 'a cada 8 horas', 8, True
    Q12H = '12/12h', 'a cada 12 horas', 12, True
    QD = '24/24h', 'a cada 24 horas', 24, True
    QOD = 'Dias Alternados', 'a cada 2 dias', 48, True
    QW = 'Semanal', 'por semana', 24*7, True
    QOW = 'Duas Semanas', 'a cada duas semana', 2*24*7, True
    QM = 'Mensal', 'ao mês', 24*30, True
    QOM = 'Bimestral', 'a cada dois meses', 2*24*30, True
    QY = 'Anual', 'ao ano', 24*365, True
    UD = 'Como Instruído', 'como instruído', 0, True 
    PRN = 'Caso Necessário', 'caso necessário', 0, True 

    def __str__(self) -> str:
        return self.value[0]
    
    def __int__(self):
        return self.value[2]

    def __bool__(self):
        return self.value[3]
    
    def __tuple__(self):
        return self.value
    
    @classmethod
    def value2member_map(cls):
        members = cls.__members__.values()
        return {**{e.value[0]: e for e in members}, **{e.value[1]: e for e in members}, **{(e.value[2],e.value[3]): e for e in members}}


class Permission(StrEnum):
    A = 'Permitido'
    F = 'Proibido'
    U = 'Indefinido'
    
class Right(StrEnum):
    R = 'Ler'
    W = 'Escrever'
    
class Access(StrEnum):
    P = 'Público'
    U = 'Usuário'
    A = 'Administrador'   
    
    
class Gender(StrEnum):
    M = 'Masculino'
    F = 'Feminino'
    O = 'Outro'
    N = 'Nenhum'
    

class VisitType(StrEnum):
    I = 'Inicial'
    F = 'Seguimento' # follow-up
    R = 'Retorno' # revisit 
    S = 'Sessão Individual'
    G = 'Sessão em Grupo'
    

class ActiveDrugType(TupleEnum):
    '''ActiveDrugType: name'''
    BENZODIAZEPINE = 'Benzodiazepínico'
    ANTIPSYCHOTIC = 'Antipsicótico'
    ANTIDEPRESSANT = 'Antidperessivo'
    PSYCHOSTIMULANT = 'Psicoestimulante'
    MOOD_STATILIZER = 'Estabilizador do Humor'
    NON_BENZO_ANXIOLYTIC = 'Ansiolítico Não Benzodiazepínico'
    NON_BENZO_HYPNOTIC = 'Hipnótico'
    ANTI_HYPERTENSIVE = 'Antihipertensiva'
    DIURETIC = 'Diurético'
    ANTICONVULSIVE = 'Anticonvulsivante'
    VASODILATOR = 'Vasodilatador'


class Pharmaceutical(TupleEnum):
    '''Pharmaceutical: name'''
    BIOLAB = 'Biolab'
    PFIZER = 'Pfizer'
    TAKEDA = 'Takeda'
    LUNDBECK = 'Lundbeck'
    ABBOT = 'Abbot'
    NOVARTIS = 'Novartis'
    LIBBS = 'Libbs'
    EUROFARMA = 'Eurofarma'
    ACHE = 'Aché'
    CRISTALIA = 'Cristália'
    EMS = 'EMS'
    SUPERA = 'Supera'


class RecipeType(TupleEnum):
    '''RecipeType: singular, plural, abbrev'''
    A = 'Receita A', 'Receitas A', 'A'
    B1 = 'Receita B1', 'Receitas B1', 'B1'
    B2 = 'Receita B2', 'Receitas B2', 'B2'
    C = 'Receita C', 'Receitas C', 'C'
    S = 'Receita Simples', 'Receitas Simples', 'S'


class DosageUnit(TupleEnum):
    '''DosageUnit: singular, plural, abbrev'''
    MG = 'miligrama', 'miligramas', 'mg'
    ML = 'mililitro', 'mililitros', 'mL'
    DL = 'decilitro', 'decilitros', 'dL'
    MG_PER_ML = 'miligrama por mililitro', 'miligramas por mililitro', 'mg/mL'
    MG_PER_DL = 'miligrama por decilitro', 'miligramas por decilitro', 'mg/dL'
    MCG = 'micrograma', 'microgramas', 'mcg'
    
    def __str__(self):
        return self.value[2]
    
    @property
    def abbrev(self):
        return self.value[2]


class DosageForm(TupleEnum):
    '''DosageForm: singular plural abbrev abbrev_plural'''
    CAPSULE = 'cápsula', 'cápsulas', 'cap', 'caps'
    TABLET = 'comprimido', 'comprimidos', 'cp', 'cps'
    SUBLINGUAL_TABLET = 'comprimido sublingual', 'comprimidos sublinguais', 'cp', 'cps'
    ORODISPERSIBLE_TABLET = 'comprimido orodispersível', 'comprimidos orodispersíveis', 'cp', 'cps'
    MILILITER = 'mililitro', 'mililitros', 'ml', 'ml'
    
    def __str__(self):
        return self.abbrev

    @property
    def abbrev(self):
        return self.value[2]


class DosageUse(TupleEnum):
    '''DosageUse: singular plural abbrev abbrev_plural conversion'''
    DOSAGE_FORM = None, None, None, None, 1
    DROP = 'gota', 'gotas', 'gt', 'gts', 20
    MICRODROP = 'microgota', 'microgotas', 'mcgt', 'mcgts', 60


class ActiveDrug(TupleEnum):
    '''ActiveDrug: name type recipe'''
    ALPRAZOLAM = 'Alprazolam', ActiveDrugType.BENZODIAZEPINE, RecipeType.B1
    BROMAZEPAM = 'Bromazepam', ActiveDrugType.BENZODIAZEPINE, RecipeType.B1
    CHLORDIAZEPOXIDE = 'Clordiazepóxido', ActiveDrugType.BENZODIAZEPINE, RecipeType.B1
    CLONAZEPAM = 'Clonazepam', ActiveDrugType.BENZODIAZEPINE, RecipeType.B1
    DIAZEPAM = 'Diazepam', ActiveDrugType.BENZODIAZEPINE, RecipeType.B1
    FLURAZEPAM = 'Flurazepam', ActiveDrugType.BENZODIAZEPINE, RecipeType.B1
    FLUNITRAZEPAM = 'Flunitrazepam', ActiveDrugType.BENZODIAZEPINE, RecipeType.B1
    LORAZEPAM = 'Lorazepam', ActiveDrugType.BENZODIAZEPINE, RecipeType.B1
    MIDAZOLAM = 'Midazolam', ActiveDrugType.BENZODIAZEPINE, RecipeType.B1
    ESTAZOLAM = 'Estazolam', ActiveDrugType.BENZODIAZEPINE, RecipeType.B1
    VALPROIC_ACID = 'Ácido Valpróico', ActiveDrugType.MOOD_STATILIZER, RecipeType.C
    LAMOTRIGINE = 'Lamotrigina', ActiveDrugType.MOOD_STATILIZER, RecipeType.C
    CARBAMAZEPINE = 'Carbamazepina', ActiveDrugType.MOOD_STATILIZER, RecipeType.C
    DIVALPROEX_SODIUM = 'Divalproato de Sódio', ActiveDrugType.MOOD_STATILIZER, RecipeType.C
    LITHIUM_CARBONATE = 'Carbonato de Lítio', ActiveDrugType.MOOD_STATILIZER, RecipeType.C
    ARIPIPRAZOLE = 'Aripiprazol', ActiveDrugType.ANTIPSYCHOTIC, RecipeType.C
    QUETIAPINE = 'Quetiapina', ActiveDrugType.ANTIPSYCHOTIC, RecipeType.C
    LURASIDONE = 'Lurasidona', ActiveDrugType.ANTIPSYCHOTIC, RecipeType.C
    ZIPRASIDONE = 'Ziprasidona', ActiveDrugType.ANTIPSYCHOTIC, RecipeType.C
    RISPERIDONE = 'Risperidona', ActiveDrugType.ANTIPSYCHOTIC, RecipeType.C
    HALOPERIDOL = 'Haloperidol', ActiveDrugType.ANTIPSYCHOTIC, RecipeType.C
    CLOZAPINE = 'Clozapina', ActiveDrugType.ANTIPSYCHOTIC, RecipeType.C
    OLANZAPINE ='Olanzapina', ActiveDrugType.ANTIPSYCHOTIC, RecipeType.C
    VORTIOXETINE = 'Vortioxetina', ActiveDrugType.ANTIDEPRESSANT, RecipeType.C
    LISDEXAMFETAMINE = 'Lisdexanfetamina', ActiveDrugType.PSYCHOSTIMULANT, RecipeType.A
    METHYLPHENIDATE = 'Metilfenidato', ActiveDrugType.PSYCHOSTIMULANT, RecipeType.A
    BUSPIRONE = 'Buspirona', ActiveDrugType.NON_BENZO_ANXIOLYTIC, RecipeType.C
    ZOLPIDEM = 'Zolpidem', ActiveDrugType.NON_BENZO_HYPNOTIC, RecipeType.C
    DULOXETINE = 'Duloxetina', ActiveDrugType.ANTIDEPRESSANT, RecipeType.C
    LOSARTAN = 'Losartana', ActiveDrugType.ANTIDEPRESSANT, RecipeType.S
    HYDROCHLOROTHIAZIDE = 'Hidroclorotiazida', ActiveDrugType.DIURETIC, RecipeType.S
    BUPROPION = 'Bupropiona', ActiveDrugType.ANTIDEPRESSANT, RecipeType.C
    MIRTAZAPINE = 'Mirtazapina', ActiveDrugType.ANTIDEPRESSANT, RecipeType.C
    PREGABALIN = 'Pregabalina', ActiveDrugType.NON_BENZO_ANXIOLYTIC, RecipeType.C
    DESVENLAFAXINE = 'Desvenlafaxina', ActiveDrugType.ANTIDEPRESSANT, RecipeType.C
    TADALAFIL = 'Tadalafila', ActiveDrugType.VASODILATOR, RecipeType.S
    ESCITALOPRAM = 'Escitalopram', ActiveDrugType.ANTIDEPRESSANT, RecipeType.C


class Brand(TupleEnum):
    '''Brand: name drugs presentations dosage_unit dosage_form dosage_usage pharmaceutical'''
    BRINTELLIX = 'Brintellix', [ActiveDrug.VORTIOXETINE], [(5,30),(10,30),(10,60),(15,30),(15,60),(20,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.LUNDBECK
    VENVANSE = 'Venvanse', [ActiveDrug.LISDEXAMFETAMINE], [(30,28),(50,28),(70,28)], DosageUnit.MG, DosageForm.CAPSULE, DosageUse.DOSAGE_FORM, Pharmaceutical.TAKEDA
    RITALIN = 'Ritalina', [ActiveDrug.METHYLPHENIDATE], [(10,20),(10,30),(10,60)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.NOVARTIS
    RITALINALA = 'Ritalina LA', [ActiveDrug.METHYLPHENIDATE], [(10,30),(20,30),(30,30),(40,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.NOVARTIS
    ARPEJO = 'Arpejo', [ActiveDrug.ARIPIPRAZOLE], [(20,30)], DosageUnit.MG_PER_ML, DosageForm.MILILITER, DosageUse.DROP, Pharmaceutical.EMS
    CYMBI = 'Cymbi', [ActiveDrug.DULOXETINE], [(30,30),(30,60),(60,30),(60,60)], DosageUnit.MG, DosageForm.CAPSULE, DosageUse.DOSAGE_FORM, Pharmaceutical.EMS
    VELIJA = 'Velija', [ActiveDrug.DULOXETINE], [(30,30),(30,60),(60,30),(60,60)], DosageUnit.MG, DosageForm.CAPSULE, DosageUse.DOSAGE_FORM, Pharmaceutical.LIBBS
    BUPIUMXL = 'Bupium XL', [ActiveDrug.BUPROPION], [(150,30),(150,60),(300,30),(300,60)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.EMS
    BUPXL = 'Bup XL', [ActiveDrug.BUPROPION], [(150,30),(300,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.EUROFARMA
    ZETRONXL = 'Zetron XL', [ActiveDrug.BUPROPION], [(150,30),(150,60),(300,30),(300,60)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM,Pharmaceutical.LIBBS
    JUNEVE = 'Juneve', [ActiveDrug.LISDEXAMFETAMINE], [(30,28),(50,28),(70,28)], DosageUnit.MG, DosageForm.CAPSULE, DosageUse.DOSAGE_FORM, Pharmaceutical.TAKEDA
    MENELAT = 'Menelat', [ActiveDrug.MIRTAZAPINE], [(30,28),(50,28),(70,28)], DosageUnit.MG, DosageForm.CAPSULE, DosageUse.DOSAGE_FORM, Pharmaceutical.TAKEDA
    APICE = 'Ápice', [ActiveDrug.PREGABALIN], [(75,30),(150,30)], DosageUnit.MG, DosageForm.CAPSULE, DosageUse.DOSAGE_FORM, Pharmaceutical.SUPERA
    ARADOISH = 'Aradois H', [ActiveDrug.LOSARTAN, ActiveDrug.HYDROCHLOROTHIAZIDE], [((50,12.5),30),((50,12.5),60)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.BIOLAB
    PATZSL = 'Patz Sl', [ActiveDrug.ZOLPIDEM], [(5,20), (5,30), (5,60)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.BIOLAB
    PRISTIQ = 'Pristiq', [ActiveDrug.DESVENLAFAXINE], [(5,20), (5,30), (5,60)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.BIOLAB
    TADALAFIL = None, [ActiveDrug.TADALAFIL], [(5,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.EUROFARMA
    ATTENZE = 'Attenze', [ActiveDrug.METHYLPHENIDATE], [(10,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.EUROFARMA
    CARBOLITIUM = 'Carbolitium', [ActiveDrug.LITHIUM_CARBONATE], [(300,50)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.EUROFARMA
    CARBOLITIUMCR = 'Carbolitium CR', [ActiveDrug.LITHIUM_CARBONATE], [(450,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.EUROFARMA
    ESC = 'ESC', [ActiveDrug.ESCITALOPRAM], [(20,60),(10,60),(15,60),(20,30),(10,30),(15,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.EUROFARMA
    ESCSOL = 'ESC Gotas', [ActiveDrug.ESCITALOPRAM], [(15,20)], DosageUnit.MG_PER_ML, DosageForm.MILILITER, DosageUse.DROP, Pharmaceutical.EUROFARMA
    QUETXR = 'Quet XR', [ActiveDrug.QUETIAPINE], [(50,30),(200,30),(300,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.EUROFARMA
    QUET = 'Quet', [ActiveDrug.QUETIAPINE], [(25,30),(200,30),(100,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.EUROFARMA
    ATIP = 'Atip', [ActiveDrug.QUETIAPINE], [(25,30),(200,30),(100,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.SUPERA
    ATIPXR = 'Atip XR', [ActiveDrug.QUETIAPINE], [(50,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.SUPERA
    ARISTAB = 'Aristab', [ActiveDrug.ARIPIPRAZOLE], [(10,30),(15,30),(20,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.ACHE
    TURNOSL = 'Turno Sl', [ActiveDrug.ZOLPIDEM], [(5,30)], DosageUnit.MG, DosageForm.TABLET, DosageUse.DOSAGE_FORM, Pharmaceutical.EUROFARMA

    
    @property
    def brand_name(self):
        val = self.value[0]
        return val if not val in ['', None] else 'Genérico'
    
    @property
    def drugs(self):
        return '/'.join([x.value[0] for x in self.value[1]]) 
    
    @property
    def presentations(self):
        result = []
        for item in self.value[2]:
            if isinstance(item[0], tuple):
                total = '+'.join([f"{x}{self.dosage_unit}" for x in item[0]])
            else:
                total = f'{item[0]}{self.dosage_unit}'
            result.append((self.brand_name, self.drugs, total, f"{item[1]}{self.dosage_form}", self.dosage_usage))
        return result 
    
    @property
    def dosage_unit(self):
        return self.value[3].abbrev
    
    @property
    def dosage_form(self):
        return self.value[4].abbrev
    
    @property
    def dosage_usage(self):
        return self.value[5].value[0] or self.dosage_form
    
    @property
    def pharmaceutical(self):
        return self.value[6].value[0]
    
    
class Drug(TupleEnum):
    _ignore_ = 'Drug brand Brand item name'
    Drug = vars()
    for brand in Brand.__members__.values():
        for item in brand.presentations:
            name = utils.remove_accents(f'{item[0]}{item[2]}{item[3]}').upper().replace(" ","").replace("/","").replace(".", "&").replace("+","")
            Drug[name] = item[0], item[1], item[2], item[3]
            
    def __str__(self):
        if self.value[0] in ['Genérico']:
            return f"{self.value[1]} {self.value[2]} {self.value[3]}"
        return f"{self.value[0]} ({self.value[1]}) {self.value[2]} {self.value[3]}"


class Experience(TupleEnum):
    _ignore_ = 'Experience data i start index names'
    Experience = vars()
    names = ['N3', 'N2', 'N1', 'E0', 'P1', 'P2', 'P3']
    data = ['Péssima', 'Muito Negativa', 'Negativa', 'Indiferente', 'Positiva', 'Muito Positiva', 'Excelente']
    start = -3
    index = 0
    Experience['UN'] = None, '---'
    for i in names:
        Experience[i] = start, data[index]
        start += 1
        index += 1
        
Experience.str = lambda x: f"{x.value[1]}"
Experience.int = lambda x: f"{x.value[0]}"



class BodySystem(StrEnum):
    CAR = 'Cardiovascular'
    RES = 'Respiratório'
    NEU = 'Nervoso'
    CIR = 'Circulatório'
    MSK = 'Musculoesquelético'
    DIG = 'Digestivo'
    SEX = 'Reprodutor'
    AUD = 'Auditório'
    VIS = 'Visual'
    TEG = 'Tegumentar'
    END = 'Endocrinológico'
    EXC = 'Excretor'
    
    
@cache
def get_cid10data_from_csv(csv_file):
    data = {}
    with open(csv_file) as file:
        for item in csv.DictReader(file, fieldnames=['code', 'title']):
            data[item['code']] = item['title']
        return data 


class Cid10Enum(BaseEnum):
    _ignore_ = 'Cid10Enum key value' 
    Cid10Enum = vars()
    for key, value in get_cid10data_from_csv(settings.CID10_FILE).items():
        Cid10Enum[key] = value