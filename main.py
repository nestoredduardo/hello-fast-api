#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI, Header, UploadFile
from fastapi import Body, Query, Path, Form, Header, Cookie, File
from fastapi import status

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
  
class LoginOut(BaseModel):
  username: str = Field(..., max_length=20, example='elmartillo')
  message: str=Field(example='Login succesfully :)')

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

#Form
@app.post(
  path='/login',
  response_model=LoginOut,
  status_code=status.HTTP_200_OK
  )
def login(username: str=Form(...), password: str=Form(...)):
  return LoginOut(username=username, message='Success')

#Cookies and Header Parameters
@app.post(
  path='/contact',
  status_code=status.HTTP_200_OK
)
def contact(
  first_name: str = Form(
    ...,
    max_length=20,
    min_length=1
  ),
  last_name: str = Form(
    ...,
    max_length=20,
    min_length=1
  ),
  email: EmailStr = Form(...),
  message: str = Form(
    ...,
    min_length=20
  ),
  user_agent: Optional[str] = Header(default=None),
  ads: Optional[str] = Cookie(default=None)
):
  return user_agent

#Files
@app.post(
  path='/post-image'
)
def post_image(
  image: UploadFile = File(...)
):
  return {
    'Filename': image.filename,
    'Format': image.content_type,
    'Size(kb)': round(len(image.file.read()) / 1024, ndigits=2)
  }