import datetime as dt
from linecache import lazycache
from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, column
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from database import Base

## Model para la tabla Alumnos
class Alumnos(Base):
    __tablename__ = 'alumnos'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    last_name = Column(String)
    date_birth = Column(DateTime) 
    date_created = Column(DateTime, default=dt.datetime.utcnow)
    phone_number = Column(Integer)
    address = Column(String)
    email = Column(String, unique=True, index=True)
    
## Model para la tabla Carreras
class Carreras(Base):
    __tablename__ = 'carreras'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

## Model para la tabla Materias
class Materias(Base):
    __tablename__ = 'materias'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

## Model para la tabla Cursadas
class Cursadas(Base):
    __tablename__ = 'cursadas'
    id = Column(Integer, primary_key=True, index=True)
    id_alumnos = Column(Integer, ForeignKey('alumnos.id', ondelete='CASCADE'))
    id_carreras = Column(Integer, ForeignKey('carreras.id', ondelete='CASCADE'))
    id_materias = Column(Integer, ForeignKey('materias.id', ondelete='CASCADE'))
    dt_inscripcion = Column(DateTime, default=dt.datetime.utcnow)
    cursada_at = Column(Integer, default=1) ## CANTIDAD DE VECES CURSADA
    
    alumnos = relationship('Alumnos',backref=backref('cursadas',lazy=True))
    carreras = relationship('Carreras',backref=backref('cursadas',lazy=True))
    materias = relationship('Materias',backref=backref('cursadas',lazy=True))

    alumno_name = association_proxy(target_collection='alumnos',attr='full_name')
    carrera_name = association_proxy(target_collection='carreras',attr='name')
    materia_name = association_proxy(target_collection='materias',attr='name')

