from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from typing import List
from schemas import BaseAlumnos, BaseCarreras, BaseCursadas, BaseMaterias, CreateAlumno, CreateCarrera, CreateCursada, CreateMateria
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

def calc_time(date: datetime):
    segundos = (date - datetime.now()).total_seconds() * -1
    dias = int(segundos / 60 / 60 / 24)
    segundos -= dias * 60 * 60 * 24
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    return f"{dias} días, {horas} horas, {minutos} minutos y {round(segundos)} segundos"

## METODOS PARA ALUMNOS
@app.post('/alumnos', response_model=BaseAlumnos, tags=['alumnos'])
async def create_alumno(alumno: CreateAlumno, db = Depends(srv.get_db)):

    return await srv.create_alumnos(alumno=alumno, db=db)

@app.get('/alumnos', response_model=List[BaseAlumnos], tags=['alumnos'])
async def get_alumnos(db = Depends(srv.get_db)):

    alumnos = []
    for x in await srv.get_all_alumnos(db=db):

        cursadas=await srv.get_cursadas_byalumno(id=x.id, db=db)
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
            cursadas={cursada.id:{'carrera':(await srv.get_carreras_byid(id=cursada.id_carreras,db=db)).name, 'materia':(await srv.get_materias_byid(id=cursada.id_materias,db=db)).name} for cursada in cursadas}
            )
            )
    
    return alumnos

@app.get('/alumnos/{id}', response_model=BaseAlumnos, tags=['alumnos'])
async def get_alumno(id: int ,db = Depends(srv.get_db)):
    alumno = await srv.get_alumno_byid(id=id, db=db)

    if alumno is None:
        raise HTTPException(status_code=404, detail='Alumno not found')

    cursadas=await srv.get_cursadas_byalumno(id=id, db=db)
    res = BaseAlumnos(
            id=alumno.id, 
            full_name=alumno.full_name, 
            last_name=alumno.last_name, 
            date_birth=alumno.date_birth,    
            phone_number=alumno.phone_number,
            address=alumno.address,
            email=alumno.email,
            date_at=calc_time(alumno.date_created),
            cursadas={x.id:{'carrera':(await srv.get_carreras_byid(id=x.id_carreras,db=db)).name, 'materia':(await srv.get_materias_byid(id=x.id_materias,db=db)).name} for x in cursadas}
            )

    return res

@app.delete('/alumnos/{id}', tags=['alumnos'])
async def del_alumno(id: int ,db = Depends(srv.get_db)):
    alumno = await srv.get_alumno_byid(id=id,db=db)

    if alumno is None:
        raise HTTPException(status_code=404, detail='Alumno not found')

    await srv.delete_alumno(alumno=alumno, db=db)

    return 'Success'

@app.put('/alumnos/{id}', response_model=BaseAlumnos, tags=['alumnos'])
async def update_alumno(id: int, data: BaseAlumnos, db = Depends(srv.get_db)):
    alumno = await srv.get_alumno_byid(id=id, db=db)

    if alumno is None:
        raise HTTPException(status_code=404, detail='Alumno not found')

    return await srv.update_alumnos(alumno=alumno, data=data, db=db)


## METODOS PARA CARRERAS
@app.post('/carreras', response_model=BaseCarreras, tags=['carreras'])
async def create_carrera(carrera: CreateCarrera, db: Session = Depends(srv.get_db)):

    return await srv.create_carreras(carrera=carrera, db=db)

@app.get('/carreras', response_model=List[BaseCarreras], tags=['carreras'])
async def get_carreras(db = Depends(srv.get_db)):

    return await srv.get_all_carreras(db=db)

@app.get('/carreras/{id}', response_model=BaseCarreras, tags=['carreras'])
async def get_carrera(id: int ,db = Depends(srv.get_db)):
    carrera = await srv.get_carreras_byid(id=id, db=db)

    if carrera is None:
        raise HTTPException(status_code=404, detail='Carrera not found')

    return carrera

@app.delete('/carreras/{id}', tags=['carreras'])
async def del_carrera(id: int ,db = Depends(srv.get_db)):
    carrera = await srv.get_carreras_byid(id=id, db=db)

    if carrera is None:
        raise HTTPException(status_code=404, detail='Carrera not found')

    await srv.delete_carrera(carrera=carrera, db=db)

    return 'Success'

@app.put('/carreras/{id}', tags=['carreras'])
async def update_carrera(id: int, data: BaseCarreras, db = Depends(srv.get_db)):
    carrera = await srv.get_carreras_byid(id=id, db=db)
    if carrera is None:
        raise HTTPException(status_code=404, detail='Carrera not found')

    return await srv.update_carrera(carreras=carrera, data=data, db=db)



## METODOS PARA MATERIAS
@app.post('/materias', response_model=BaseMaterias, tags=['materias'])
async def create_materias(materias: CreateMateria, db: Session = Depends(srv.get_db)):

    return await srv.create_materias(materia=materias, db=db)

@app.get('/materias', response_model=List[BaseMaterias], tags=['materias'])
async def get_materias(db = Depends(srv.get_db)):

    return await srv.get_all_materias(db=db)

@app.get('/materias/{id}', response_model=BaseMaterias, tags=['materias'])
async def get_materia(id: int ,db = Depends(srv.get_db)):
    materia = await srv.get_materias_byid(id=id, db=db)

    if materia is None:
        raise HTTPException(status_code=404, detail='Materia not found')

    return materia

@app.delete('/materias/{id}', tags=['materias'])
async def del_materias(id: int ,db = Depends(srv.get_db)):
    materias = await srv.get_materias_byid(id=id, db=db)

    if materias is None:
        raise HTTPException(status_code=404, detail='Materia not found')

    await srv.delete_materias(materia=materias, db=db)

    return 'Success'

@app.put('/materias/{id}', tags=['materias'])
async def update_materias(id: int, data: BaseMaterias, db = Depends(srv.get_db)):
    materias = await srv.get_materias_byid(id=id, db=db)
    if materias is None:
        raise HTTPException(status_code=404, detail='Materia not found')

    return await srv.update_materias(materias=materias, data=data, db=db)




## METODOS PARA CURSADAS
@app.post('/cursadas', response_model=BaseCursadas, tags=['cursadas'])
async def create_cursadas(cursada: CreateCursada, db: Session = Depends(srv.get_db)):

    return await srv.create_cursadas(cursada=cursada, db=db)

@app.get('/cursadas', response_model=List[BaseCursadas], tags=['cursadas'])
async def get_cursadas(db = Depends(srv.get_db)):

    cursadas = await srv.get_all_cursadas(db=db)
    alumno = (await srv.get_alumno_byid(id=cursadas[0].id_alumnos,db=db)).full_name
    print(alumno)
    return await srv.get_all_cursadas(db=db)

@app.get('/cursadas/{id}', response_model=BaseCursadas, tags=['cursadas'])
async def get_cursada(id: int ,db = Depends(srv.get_db)):
    cursada = await srv.get_cursadas_byid(id=id, db=db)

    if cursada is None:
        raise HTTPException(status_code=404, detail='Cursada not found')

    return cursada

@app.delete('/cursadas/{id}', tags=['cursadas'])
async def del_cursada(id: int ,db = Depends(srv.get_db)):
    cursada = await srv.get_cursadas_byid(id=id, db=db)

    if cursada is None:
        raise HTTPException(status_code=404, detail='Cursada not found')

    await srv.delete_cursada(cursada=cursada, db=db)

    return 'Success'

@app.put('/cursadas/{id}', tags=['cursadas'])
async def update_cursadas(id: int, data: BaseCursadas, db = Depends(srv.get_db)):
    cursada = await srv.get_materias_byid(id=id, db=db)
    if cursada is None:
        raise HTTPException(status_code=404, detail='Cursada not found')

    return await srv.update_cursadas(cursadas=cursada, data=data, db=db)

@app.get('/create_seed_tables')
def create_seed_tables():
    print('Creando Tablas')
    srv.create_tables()
    print('Seed DB')
    srv.seed_db()

    return 'Success'