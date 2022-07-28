# ChallengeEdMachina

Challenge BackEnd con fastapi & postgres 


## Compose

`` 
docker-compose up --build
`` 

#### Puede crear las tablas con data de ejemplo desde el endpoint

`` 
** /create_seed_tables **
`` 

#### O solo crear las tablas:

`` 
** /create_tables **
`` 

## ENDPOINTS


- **/alumnos** (GET, PUT, UPDATE, DELETE)

- **/alumnos/{id}** (GET)

- **/carreras** (GET, PUT, UPDATE, DELETE)

- **/carreras/{id}** (GET)

- **/materias** (GET, PUT, UPDATE, DELETE)

- **/materias/{id}** (GET)

- **/cursadas** (GET, PUT, UPDATE, DELETE)

- **/cursadas/{id}** (GET)

## Pruebas:

Ingresar a /docs
`` 
/docs
`` 