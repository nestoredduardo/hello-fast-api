#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models
class HairColor(Enum):
  white = "white"
  brown = "brown"
  black = "black"
  blonde = "blonde"
  red = "red"

class Location(BaseModel):
  city: str
  state: str
  country: str  

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Marty'
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='McFly'
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example='20'
        )
    hair_color: Optional[HairColor] = Field(default=None, example='black')
    is_married: Optional[bool] = Field(default=None, example='False')
    class Config:
        orm_mode = True

class Person(PersonBase):
  password: str = Field(
    ...,
    min_length=6
  )

class PersonOut(PersonBase):
  pass
  


@app.get('/')
def home():
  return {'Hello': 'World'}


#Request and response body

@app.post('/person/new', response_model= PersonOut)
def create_person(person: Person = Body(...)): # 3 puntos significa necesario
  return person

#Validaciones: Query Parameters
@app.get('/person/details')
def show_person(
  name: Optional[str] = Query(
    None, 
    min_length=1, 
    max_length=50, 
    title='Person Name', 
    description="This is the person name. It's between 1 and 50 char",
    example="Edu"
    ),
  age: int = Query(
    ..., 
    ge=0, 
    le=120,
    example=21
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
  person: Person = Body(...)
  #location: Location = Body(...)
):
  #results = person.dict()
  #results.update(location.dict())
  return person