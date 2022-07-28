from datetime import datetime
from email.policy import default
from typing import Optional
from unicodedata import name
from pydantic import BaseModel

class BaseAlumnos(BaseModel):
    id: Optional[int]
    full_name: str
    last_name: str
    date_birth: datetime
    phone_number: int
    address: str
    email: str
    date_at: Optional[str]
    date_created: Optional[datetime]
    cursadas: Optional[dict]

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

    class Config:
        orm_mode = True

class CreateCarrera(BaseModel):
    name: str
    description:str
    materias:int = 0
    class Config:
        orm_mode = True

class BaseMaterias(BaseModel):
    id: Optional[int]
    name: str
    description: str

    class Config:
        orm_mode = True

class CreateMateria(BaseModel):
    name:str
    description:str 

    class Config:
        orm_mode = True

class BaseCursadas(BaseModel):
    id: Optional[int]
    id_alumnos: int
    id_carreras: int
    id_materias: int
    dt_inscripcion: datetime
    cursada_at: int

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