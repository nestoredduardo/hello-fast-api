#Python
from operator import gt
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models
class Location(BaseModel):
  city: str
  state: str
  country: str

class Person(BaseModel):
  firts_name: str
  last_name: str
  age: int
  hair_color: Optional[str] = None
  is_married: Optional[bool] = None

@app.get('/')
def home():
  return {'Hello': 'World'}


#Request and response body

@app.post('/person/new')
def create_person(person: Person = Body(...)): # 3 puntos significa necesario
  return Person

#Validaciones: Query Parameters
@app.get('/person/details')
def show_person(
  name: Optional[str] = Query(
    None, 
    min_length=1, 
    max_length=50, 
    title='Person Name', 
    description="This is the person name. It's between 1 and 50 char"
    ),
  age: int = Query(
    ..., 
    ge=0, 
    le=120
    )
):
  return {name: age}

#Validaciones: Path Parameters
@app.get('/person/detail/{person_id}')
def show_person(
  person_id: int = Path(
    ..., 
    gt=0,
    title="Person Id Validation",
    description="Return if a person_id exist"
    )
):
  return {person_id: True}

#Validaciones: Request body
@app.put('/person/{person_id}')
def update_person(
  person_id: int = Path(...,
    title='Put Person Id',
    description="Update Person Data",
    gt=0
  ),
  person: Person = Body(...),
  location: Location = Body(...)
):
  results = person.dict()
  results.update(location.dict())
  return results