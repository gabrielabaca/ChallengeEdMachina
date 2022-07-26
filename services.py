from typing import List
from database import engine, Base, SessionLocal
from schemas import BaseAlumnos, BaseCarreras, BaseCursadas, BaseMaterias, CreateAlumno, CreateCarrera, CreateCursada, CreateMateria
from sqlalchemy.orm import Session
import models as models


## UTILIDADES
def create_tables():
    return Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


## METODOS PARA LA TABLA ALUMNOS

async def create_alumnos(alumno: CreateAlumno, db: Session) -> BaseAlumnos:
    alumno = models.Alumnos(**alumno.dict())
    db.add(alumno)
    db.commit()
    db.refresh(alumno)

    return BaseAlumnos.from_orm(alumno)

async def get_all_alumnos(db: Session):
    alumnos = db.query(models.Alumnos).all()
    return list(alumnos)

async def get_alumno_byid(id: int, db: Session) -> BaseAlumnos:
    alumno = db.query(models.Alumnos).filter(models.Alumnos.id == id).first()
    return (alumno)

async def delete_alumno(alumno: models.Alumnos, db: Session):
    db.delete(alumno)
    db.commit()
    
    pass

async def update_alumnos(alumno: models.Alumnos, data: BaseAlumnos, db: Session):
    alumno.full_name = data.full_name
    alumno.last_name = data.last_name
    alumno.date_birth = data.date_birth
    alumno.phone_number = data.phone_number
    alumno.address = data.address
    alumno.email = data.email

    db.commit()
    db.refresh(alumno)

    return alumno


## METODOS PARA LA TABLA CARRERAS

async def create_carreras(carrera: CreateCarrera, db: Session) -> BaseCarreras:
    carrera = models.Carreras(**carrera.dict())
    db.add(carrera)
    db.commit()
    db.refresh(carrera)

    return BaseCarreras.from_orm(carrera)

async def get_all_carreras(db: Session) -> list[BaseCarreras]:
    carreras = db.query(models.Carreras).all()
    return list(map(BaseCarreras.from_orm, carreras))

async def get_carreras_byid(id: int, db: Session) -> BaseCarreras:
    carrera = db.query(models.Carreras).filter(models.Carreras.id == id).first()
    return (carrera)

async def delete_carrera(carrera: models.Carreras, db: Session):
    db.delete(carrera)
    db.commit()
    
    pass

async def update_carrera(carreras: models.Carreras, data: BaseCarreras, db: Session):
    carreras.name = data.name
    carreras.materias = data.materias
    carreras.description = data.description

    db.commit()
    db.refresh(carreras)

    return carreras


## METODOS PARA LA TABLA MATERIAS

async def create_materias(materia: CreateMateria, db: Session) -> BaseMaterias:
    materia = models.Materias(**materia.dict())
    db.add(materia)
    db.commit()
    db.refresh(materia)

    return BaseMaterias.from_orm(materia)

async def get_all_materias(db: Session) -> list[BaseMaterias]:
    materias = db.query(models.Materias).all()
    return list(map(BaseMaterias.from_orm, materias))

async def get_materias_byid(id: int, db: Session) -> BaseMaterias:
    materia = db.query(models.Materias).filter(models.Materias.id == id).first()
    return (materia)

async def delete_materias(materia: models.Materias, db: Session):
    db.delete(materia)
    db.commit()
    
    pass

async def update_materias(materias: models.Materias, data: BaseMaterias, db: Session):
    materias.name = data.name
    materias.description = data.description

    db.commit()
    db.refresh(materias)

    return materias


## METODOS PARA LA TABLA CURSADAS

async def create_cursadas(cursada: CreateCursada, db: Session) -> BaseCursadas:
    cursada = models.Cursadas(**cursada.dict())
    db.add(cursada)
    db.commit()
    db.refresh(cursada)

    return BaseCursadas.from_orm(cursada)

async def get_all_cursadas(db: Session) -> list[BaseCursadas]:
    cursadas = db.query(models.Cursadas).all()
    return list(map(BaseCursadas.from_orm, cursadas))

async def get_cursadas_byalumno(id: int, db:Session) -> BaseCursadas:
    cursada = db.query(models.Cursadas).filter(models.Cursadas.id_alumnos == id)
    return list(cursada)

async def get_cursadas_byid(id: int, db: Session) -> BaseCursadas:
    cursada = db.query(models.Cursadas).filter(models.Cursadas.id == id).first()
    return (cursada)

async def delete_cursada(cursada: models.Cursadas, db: Session):
    db.delete(cursada)
    db.commit()
    
    pass

async def update_cursadas(cursadas: models.Cursadas, data: BaseCursadas, db: Session):
    cursadas.name = data.name
    cursadas.description = data.description

    db.commit()
    db.refresh(cursadas)

    return cursadas