from datetime import datetime
from typing import List
from fastapi import Depends, HTTPException
from database import engine, Base, SessionLocal
from schemas import BaseAlumnos, BaseCarreras, BaseCursadas, BaseMaterias, CreateAlumno, CreateCarrera, CreateCursada, CreateMateria
from sqlalchemy.orm import Session
import models as models
import random

## UTILIDADES
def create_tables():
    return Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_db(db:Session = SessionLocal()):
    alumnos = [
        {'full_name':'Lucio Gabriel', 'last_name':'Abaca', 'date_birth':'1991-10-16', 'phone_number':'1169759327','address':'Milazzo 5005', 'email':'gabrielabaca@live.com.ar'},
        {'full_name':'Nombre 2', 'last_name':'Apellido 2', 'date_birth':'1991-10-16', 'phone_number':'1169759327','address':'Milazzo 5005', 'email':'email@live.com.ar'},
        {'full_name':'Nombre 3', 'last_name':'Apellido 3', 'date_birth':'1991-10-16', 'phone_number':'1169759327','address':'Milazzo 5005', 'email':'email2@live.com.ar'},
        {'full_name':'Nombre 4', 'last_name':'Apellido 4', 'date_birth':'1991-10-16', 'phone_number':'1169759327','address':'Milazzo 5005', 'email':'email3@live.com.ar'},
        {'full_name':'Nombre 5', 'last_name':'Apellido 5', 'date_birth':'1991-10-16', 'phone_number':'1169759327','address':'Milazzo 5005', 'email':'email4@live.com.ar'},
        {'full_name':'Nombre 6', 'last_name':'Apellido 6', 'date_birth':'1991-10-16', 'phone_number':'1169759327','address':'Milazzo 5005', 'email':'email5@live.com.ar'},
        {'full_name':'Nombre 7', 'last_name':'Apellido 7', 'date_birth':'1991-10-16', 'phone_number':'1169759327','address':'Milazzo 5005', 'email':'email6@live.com.ar'},
    ]
    id_alumnos = []

    materias = [
        {'name':'Matematicas','description':'Nueva Materia Matematicas'},
        {'name':'Fisica','description':'Nueva Materia Fisica'},
        {'name':'Quimica','description':'Nueva Materia Quimica'},
        {'name':'Filosofia','description':'Nueva Materia Filosofia'},
        {'name':'Biologia','description':'Nueva Materia Biologia'},
        {'name':'Historia','description':'Nueva Materia Historia'},
        {'name':'Anatomia','description':'Nueva Materia Anatomia'},
        {'name':'Matematicas 2','description':'Nueva Materia Matematicas 2'},
        {'name':'Derechos Humanos','description':'Nueva Materia Derechos Humanos'},
        {'name':'Lenguaje','description':'Nueva Materia Lenguaje'},
    ]
    id_materias = []

    carreras = [
        {'name':'Carrera de Matematicas','description':'Esta es una carrera'},
        {'name':'Carrera de Lenguas','description':'Esta es otra carrera'},
        {'name':'Carrera de Diseño','description':'Esta es otra carrera mas'},
    ]
    id_carreras = []

    for dato in alumnos:
        datatosave = models.Alumnos()
        
        datatosave.full_name = dato['full_name']
        datatosave.last_name = dato['last_name']
        datatosave.date_birth = dato['date_birth']
        datatosave.phone_number = dato['phone_number']
        datatosave.address = dato['address']
        datatosave.email = dato['email']
        
        db.add(datatosave)
        db.commit()
        db.refresh(datatosave)
        id_alumnos.append(datatosave.id)
        print(f'Alumno { datatosave.last_name }, { datatosave.full_name } creado con ID: { datatosave.id }')

    for dato in materias:
        datatosave = models.Materias()

        datatosave.name = dato['name']
        datatosave.description = dato['description']

        db.add(datatosave)
        db.commit()
        db.refresh(datatosave)
        id_materias.append(datatosave.id)
        print(f'Materia { datatosave.name } creada con ID: { datatosave.id }')

    for dato in carreras:
        datatosave = models.Carreras()

        datatosave.name = dato['name']
        datatosave.description = dato['description']

        db.add(datatosave)
        db.commit()
        db.refresh(datatosave)
        id_carreras.append(datatosave.id)
        print(f'Carrera { datatosave.name } creada con ID: { datatosave.id }')

    i = 0
    while i < 50:
        datatosave = models.Cursadas()

        
        datatosave.id_alumnos = id_alumnos[random.randrange(len(id_alumnos))]
        datatosave.id_carreras = id_carreras[random.randrange(len(id_carreras))]
        datatosave.id_materias = id_materias[random.randrange(len(id_materias))]
        datatosave.cursada_at = random.choice(range(1,5))

        db.add(datatosave)
        db.commit()
        db.refresh(datatosave)
        print(f'Cursada { datatosave.id } creada')

        i += 1

    db.close()
    pass

def calc_time(date: datetime):
    segundos = (date - datetime.now()).total_seconds() * -1
    dias = int(segundos / 60 / 60 / 24)
    segundos -= dias * 60 * 60 * 24
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    return f"{dias} días, {horas} horas, {minutos} minutos y {round(segundos)} segundos"

## METODOS PARA LA TABLA ALUMNOS

async def create_alumnos(alumno: CreateAlumno, db: Session) -> BaseAlumnos:
    alumno = models.Alumnos(**alumno.dict())
    db.add(alumno)
    db.commit()
    db.refresh(alumno)

    return BaseAlumnos.from_orm(alumno)

async def get_all_alumnos(db:Session):
    
    alumnos = []
    for x in db.query(models.Alumnos).all():
        cursadas=await get_cursadas_byalumno(id=x.id, db=db)
        alumnos.append(BaseAlumnos(
            id=x.id, 
            full_name=x.full_name,  
            last_name=x.last_name, 
            date_birth=x.date_birth,    
            phone_number=x.phone_number,
            address=x.address,
            email=x.email,
            date_created=x.date_created,
            date_at=calc_time(x.date_created),  
            cursadas={cursada.id:{'carrera':(await get_carreras_byid(id=cursada.id_carreras,db=db)).name, 'materia':(await get_materias_byid(id=cursada.id_materias,db=db)).name} for cursada in cursadas}
            )
            )
    
    return list(alumnos)

async def get_alumno_byid(id: int, db:Session) ->BaseAlumnos:
    data = db.query(models.Alumnos).filter(models.Alumnos.id == id).first()
    
    if data is None:
        raise HTTPException(status_code=404, detail='Alumno not found')

    cursadas=await get_cursadas_byalumno(id=id, db=db)
    alumno = BaseAlumnos(
            id=data.id, 
            full_name=data.full_name, 
            last_name=data.last_name, 
            date_birth=data.date_birth,    
            phone_number=data.phone_number,
            address=data.address,
            email=data.email,
            date_at=calc_time(data.date_created),
            cursadas={x.id:{'carrera':(await get_carreras_byid(id=x.id_carreras,db=db)).name, 'materia':(await get_materias_byid(id=x.id_materias,db=db)).name} for x in cursadas}
            )
            
    return alumno
    
async def delete_alumno(id: int, db: Session):

    alumno = db.query(models.Alumnos).filter(models.Alumnos.id == id).first()

    if alumno is None:
        raise HTTPException(status_code=404, detail='Alumno not found')

    db.delete(alumno)
    db.commit()
    
    return 'Success'
    

async def update_alumnos(id: int, data: BaseAlumnos, db: Session) -> BaseAlumnos:
    alumno = db.query(models.Alumnos).filter(models.Alumnos.id == id).first()

    if alumno is None:
        raise HTTPException(status_code=404, detail="Alumno not found")

    alumno.full_name = data.full_name
    alumno.last_name = data.last_name
    alumno.date_birth = data.date_birth
    alumno.phone_number = data.phone_number
    alumno.address = data.address
    alumno.email = data.email

    db.commit()
    db.refresh(alumno)

    return BaseAlumnos.from_orm(alumno)


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
    if carrera is None:
        raise HTTPException(status_code=404, detail='Carrera not found')

    return BaseCarreras.from_orm(carrera)

async def delete_carrera(id: int, db: Session):
    carrera = db.query(models.Carreras).filter(models.Carreras.id == id).first()
    if carrera is None:
        raise HTTPException(status_code=404, detail='Carrera not found')

    db.delete(carrera)
    db.commit()
    
    return 'Success'

async def update_carrera(id: int, data: BaseCarreras, db: Session) -> BaseCarreras:
    carrera = db.query(models.Carreras).filter(models.Carreras.id == id).first()
    if carrera is None:
        raise HTTPException(status_code=404, detail='Carrera not found')

    carrera.name = data.name
    carrera.description = data.description

    db.commit()
    db.refresh(carrera)

    return BaseCarreras.from_orm(carrera)


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

    if materia is None:
        raise HTTPException(status_code=404, detail='Materia not found')

    return BaseMaterias.from_orm(materia)

async def delete_materias(id: int, db: Session):

    materia = db.query(models.Materias).filter(models.Materias.id == id).first()

    if materia is None:
        raise HTTPException(status_code=404, detail='Materia not found')

    db.delete(materia)
    db.commit()
    
    return 'Success'

async def update_materias(id: id, data: BaseMaterias, db: Session) -> BaseMaterias:
    materias =  db.query(models.Materias).filter(models.Materias.id == id).first()
    
    if materias is None:
        raise HTTPException(status_code=404, detail='Materia not found')
    materias.name = data.name
    materias.description = data.description

    db.commit()
    db.refresh(materias)

    return BaseMaterias.from_orm(materias)


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
    return BaseCursadas.from_orm(cursada)

async def get_cursadas_byid(id: int, db: Session) -> BaseCursadas:

    cursada = db.query(models.Cursadas).filter(models.Cursadas.id == id).first()

    if cursada is None:
        raise HTTPException(status_code=404, detail='Cursada not found')

    return BaseCursadas.from_orm(cursada)

async def delete_cursada(id: int, db: Session):

    cursada = db.query(models.Cursadas).filter(models.Cursadas.id == id).first()

    if cursada is None:
        raise HTTPException(status_code=404, detail='Cursada not found')

    db.delete(cursada)
    db.commit()
    
    return 'Success'

async def update_cursadas(id: int, data: BaseCursadas, db: Session) -> BaseCursadas:

    cursadas = db.query(models.Cursadas).filter(models.Cursadas.id == id).first()

    if cursadas is None:
        raise HTTPException(status_code=404, detail='Cursada not found')
        
    cursadas.id_alumnos = data.id_alumnos
    cursadas.id_carreras = data.id_carreras
    cursadas.id_materias = data.id_materias
    cursadas.dt_inscripcion = data.dt_inscripcion
    cursadas.cursada_at = data.cursada_at

    db.commit()
    db.refresh(cursadas)

    return BaseCursadas.from_orm(cursadas)