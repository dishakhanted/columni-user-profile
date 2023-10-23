#
# FastAPI is a framework and library for implementing REST web services in Python.
# https://fastapi.tiangolo.com/
#
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

import uvicorn


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse("/static/index.html")

class NewProfile(BaseModel):
    user_id : int
    school_id : int
    first_name : str
    last_name : str
    columbiaEmail : str
    password : str
    profilePicture : str #url ?
    major = str
    jobTitle : Optional[str] = "NA"
    company : Optional[str] = "NA"
    graduationDate : str
    userDescription	: Optional[str] = "NA"
    creationDT : str


def storeToDb(first_name: str,last_name:str):
    return JSONResponse (
         status_code =  status.HTTP_200_OK,
         content ={
             'first_name' : first_name,
             'last_name' : last_name,
         },
    )

@app.post("/newProfile")
async def get_students(request: NewProfile):
    """
    Return a list of students matching a query string.

    - **uni**: student's UNI
    - **last_name**: student's last name
    - **school_code**: student's school.
    """
    try:
        user_id = request.user_id
        school_id = request.school_id
        first_name = request.first_name
        last_name = request.last_name
        columbiaEmail = request.columbiaEmail
        password = request.password
        profilePicture = request.profilePicture
        major  = request.major
        jobTitle = request.jobTitle
        company = request.company
        graduationDate = request.graduationDate
        userDescription	= request.userDescription
        creationDT = request.creationDT
        return storeToDb(first_name,last_name)
    except Exception as e:
        return JSONResponse (
         status_code =  status.HTTP_400_BAD_REQUEST,
         content ={
             'ERROR' : e,
         },
    )
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011)
