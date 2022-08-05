from datetime import datetime
from email.policy import default
from typing import Optional, List
from unicodedata import name
from click import option
from pydantic import BaseModel, validator


class BaseCursadas(BaseModel):
    id: Optional[int]
    dt_inscripcion: datetime

    cursada_at: int

    alumno_name: str
    materia_name: str
    carrera_name: str
    class Config:
        orm_mode = True

class BaseCursadasAll(BaseCursadas):
    id_alumnos: int
    id_carreras:int
    id_materias: int

    class Config:
        orm_mode = True
         
class CreateCursada(BaseModel):
    id_alumnos: int
    id_carreras: int
    id_materias:int
    dt_inscripcion:datetime 
    cursada_at: int 

    class Config:
        orm_mode = True

class BaseAlumnos(BaseModel):
    id: Optional[int]
    full_name: str
    last_name: str
    date_birth: datetime
    phone_number: int
    address: str
    email: str
    date_created: Optional[datetime]
    cursadas: List[BaseCursadas] = []

    class Config:
        orm_mode = True

class CreateAlumno(BaseModel):
    full_name:str 
    last_name:str 
    date_birth:datetime 
    phone_number:int 
    address: str 
    email: str 
    
    class Config:
        orm_mode: True

class BaseCarreras(BaseModel):
    id: Optional[int]
    name: str
    description: str
    cursadas: List[BaseCursadas] = []
    
    class Config:
        orm_mode = True

class CreateCarrera(BaseModel):
    name: str
    description:str
    class Config:
        orm_mode = True

class BaseMaterias(BaseModel):
    id: Optional[int]
    name: str
    description: str
    cursadas: List[BaseCursadas] = []

    class Config:
        orm_mode = True

class CreateMateria(BaseModel):
    name:str
    description:str 

    class Config:
        orm_mode = True

