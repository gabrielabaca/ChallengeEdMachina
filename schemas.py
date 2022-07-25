from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class BaseAlumnos(BaseModel):
    id: Optional[int]
    full_name: str
    last_name: str
    date_birth: datetime
    phone_number: int
    address: str
    email: str

    class Config:
        orm_mode = True

class BaseCarreras(BaseModel):
    id: Optional[int]
    name: str
    materias: int
    description: str

    class Config:
        orm_mode = True

class BaseMaterias(BaseModel):
    id: Optional[int]
    name: str
    description: str

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
