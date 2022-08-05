from fastapi import FastAPI, Depends, HTTPException
from typing import List
from schemas import BaseAlumnos, BaseCarreras, BaseCursadas, BaseCursadasAll, BaseMaterias, CreateAlumno, CreateCarrera, CreateCursada, CreateMateria
from sqlalchemy.orm import Session
import services as srv


tags_metadata = [
    {
        "name": "alumnos",
        "description": "Operaciones sobre la tabla 'alumnos'",
    },
    {
        "name": "carreras",
        "description": "Operaciones sobre la tabla 'carreras'",
    },
    {
        "name": "materias",
        "description": "Operaciones sobre la tabla 'materias'",
    },
    {
        "name": "cursadas",
        "description": "Operaciones sobre la tabla 'cursadas'",
    },
]

app = FastAPI(title='EdMachina Challenge',openapi_tags=tags_metadata)


## METODOS PARA ALUMNOS
@app.post('/alumnos', response_model=BaseAlumnos, tags=['alumnos'])
async def create_alumno(alumno: CreateAlumno, db = Depends(srv.get_db)):

    return await srv.create_alumnos(alumno=alumno, db=db)

@app.get('/alumnos', response_model=List[BaseAlumnos], tags=['alumnos'])
async def get_alumnos(db = Depends(srv.get_db)):

    return await srv.get_all_alumnos(db=db)

@app.get('/alumnos/{id}', response_model=BaseAlumnos, tags=['alumnos'])
async def get_alumno(id: int ,db = Depends(srv.get_db)):

    return await srv.get_alumno_byid(id=id,db=db)

@app.delete('/alumnos/{id}', tags=['alumnos'])
async def del_alumno(id: int ,db = Depends(srv.get_db)):

    return await srv.delete_alumno(id=id, db=db)


@app.put('/alumnos/{id}', response_model=BaseAlumnos, tags=['alumnos'])
async def update_alumno(id: int, data: BaseAlumnos, db = Depends(srv.get_db)):
    
    return await srv.update_alumnos(id=id, data=data, db=db)


## METODOS PARA CARRERAS
@app.post('/carreras', response_model=BaseCarreras, tags=['carreras'])
async def create_carrera(carrera: CreateCarrera, db: Session = Depends(srv.get_db)):

    return await srv.create_carreras(carrera=carrera, db=db)

@app.get('/carreras', response_model=List[BaseCarreras], tags=['carreras'])
async def get_carreras(db = Depends(srv.get_db)):

    return await srv.get_all_carreras(db=db)

@app.get('/carreras/{id}', response_model=BaseCarreras, tags=['carreras'])
async def get_carrera(id: int ,db = Depends(srv.get_db)):

    return await srv.get_carreras_byid(id=id, db=db)


@app.delete('/carreras/{id}', tags=['carreras'])
async def del_carrera(id: int ,db = Depends(srv.get_db)):
    
    return await srv.delete_carrera(id=id, db=db)


@app.put('/carreras/{id}', tags=['carreras'])
async def update_carrera(id: int, data: BaseCarreras, db = Depends(srv.get_db)):
    
    return await srv.update_carrera(id=id, data=data, db=db)



## METODOS PARA MATERIAS
@app.post('/materias', response_model=BaseMaterias, tags=['materias'])
async def create_materias(materias: CreateMateria, db: Session = Depends(srv.get_db)):

    return await srv.create_materias(materia=materias, db=db)

@app.get('/materias', response_model=List[BaseMaterias], tags=['materias'])
async def get_materias(db = Depends(srv.get_db)):

    return await srv.get_all_materias(db=db)

@app.get('/materias/{id}', response_model=BaseMaterias, tags=['materias'])
async def get_materia(id: int ,db = Depends(srv.get_db)):

    return await srv.get_materias_byid(id=id, db=db)

@app.delete('/materias/{id}', tags=['materias'])
async def del_materias(id: int ,db = Depends(srv.get_db)):

    return await srv.delete_materias(id=id, db=db)

@app.put('/materias/{id}', tags=['materias'])
async def update_materias(id: int, data: BaseMaterias, db = Depends(srv.get_db)):

    return await srv.update_materias(id=id, data=data, db=db)


## METODOS PARA CURSADAS
@app.post('/cursadas', response_model=BaseCursadas, tags=['cursadas'])
async def create_cursadas(cursada: CreateCursada, db: Session = Depends(srv.get_db)):

    return await srv.create_cursadas(cursada=cursada, db=db)

@app.get('/cursadas', response_model=List[BaseCursadasAll], tags=['cursadas'])
async def get_cursadas(db = Depends(srv.get_db)):

    return await srv.get_all_cursadas(db=db)

@app.get('/cursadas/{id}', response_model=BaseCursadasAll, tags=['cursadas'])
async def get_cursada(id: int ,db = Depends(srv.get_db)):

    return await srv.get_cursadas_byid(id=id, db=db)

@app.delete('/cursadas/{id}', tags=['cursadas'])
async def del_cursada(id: int ,db = Depends(srv.get_db)):

    return await srv.delete_cursada(id=id, db=db)

@app.put('/cursadas/{id}', tags=['cursadas'])
async def update_cursadas(id: int, data: BaseCursadas, db = Depends(srv.get_db)):
    
    return await srv.update_cursadas(id=id, data=data, db=db)


## Crear tablas y Data de ejemplo
@app.get('/create_seed_tables')
def create_seed_tables():
    print('Creando Tablas')
    srv.create_tables()
    print('Seed DB')
    srv.seed_db()

    return 'Success'

## Crear Tablas
@app.get('/create_tables')
def create_seed_tables():
    print('Creando Tablas')
    srv.create_tables()

    return 'Success'