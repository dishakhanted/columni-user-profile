from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel, ValidationError, validator
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

conn = psycopg2.connect(database = os.environ["PSQL_DATABASE"], #"columni_userdb", 
                        user = os.environ["PSQL_USER"], #"postgres", 
                        host = os.environ["PSQL_HOST"], # 'columni-user-db.cnuwaz8dqxjy.us-east-1.rds.amazonaws.com',
                        password = os.environ["PSQL_PASSWORD"], # "Disha101",
                        port = int(os.environ["PSQL_PORT"])) # 5432)
cursor = conn.cursor(cursor_factory=RealDictCursor)

INSERT_QUERY = "INSERT INTO users (schoolid, firstname, lastname, columbiaemail, password, profilepicture, major, jobtitle, company, graduationdate, userdescription, creationdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
GET_FROM_EMAIL = "SELECT * FROM users WHERE columbiaEmail = %s"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse("/static/index.html")

class NewProfile(BaseModel):
    userid: Optional[int]
    schoolid: int
    firstname: Optional[str] = ""
    lastname: Optional[str] = ""
    columbiaemail: str
    password: str
    profilepicture: Optional[str]  # Consider using Url type
    major: str
    jobtitle: Optional[str] = ""
    company: Optional[str] = ""
    graduationdate: int
    userdescription: Optional[str] = ""
    creationdate: Optional[datetime]  # Consider using datetime type

    @validator('creationdate', pre=False, allow_reuse=True)
    def format_datetime(cls, value):
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')

def fetchFromDb(user_id: int):
    # Placeholder for fetching data from the database
    # Ensure the fetch is for the specific user_id
    cursor.execute("SELECT * FROM users WHERE userid = %s", (user_id,))
    row = cursor.fetchone()
    conn.commit()
    if row is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "msg": "User does not exist"
            }
        )
    return NewProfile(**dict(row)).dict()


def updateDb(user_id: int, profile: NewProfile):
    # Placeholder for updating data in the database
    # Ensure the update is for the specific user_id
    cursor.execute("SELECT * FROM users WHERE userid = %s", (user_id,))
    row = cursor.fetchone()
    conn.commit()
    if row is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "msg": "User does not exist"
            }
        )
    cursor.execute("UPDATE users SET schoolid = %s, firstname = %s, lastname = %s, columbiaemail = %s, password = %s, profilepicture = %s, major = %s, jobtitle = %s, company = %s, graduationdate = %s, userdescription = %s WHERE userid = %s", (profile.schoolid, profile.firstname, profile.lastname, profile.columbiaemail, profile.password, profile.profilepicture, profile.major, profile.jobtitle, profile.company, profile.graduationdate, profile.userdescription, user_id))
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE userid = %s", (user_id,))
    row = cursor.fetchone()
    conn.commit()
    profile = NewProfile(**dict(row))
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=profile.dict()
    )

def deleteFromDb(user_id: int):
    # Placeholder for deleting data from the database
    # Ensure the delete is for the specific user_id
    cursor.execute("SELECT * FROM users WHERE userid = %s", (user_id,))
    row = cursor.fetchone()
    conn.commit()
    if row is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "msg": "User does not exist"
            }
        )
    cursor.execute("DELETE FROM users WHERE userid = %s", (user_id,))
    conn.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": f"User deleted successfully",
            "userid": user_id
        }
    )

def storeToDb(profile: NewProfile):
    # Placeholder for storing data in the database
    # Store all profile details, not just first and last name
    cursor.execute("SELECT * FROM users WHERE columbiaemail = %s", (profile.columbiaemail,))
    row = cursor.fetchone()
    if row is not None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "msg": "User already exists"
            }
        )
    cursor.execute(INSERT_QUERY, (profile.schoolid, profile.firstname, profile.lastname, profile.columbiaemail, profile.password, profile.profilepicture, profile.major, profile.jobtitle, profile.company, profile.graduationdate, profile.userdescription, datetime.now()))
    conn.commit()
    cursor.execute(GET_FROM_EMAIL, (profile.columbiaemail,))
    row = cursor.fetchall()[0]
    conn.commit()
    row = dict(row)
    p = NewProfile(**row)
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=p.dict()
    ) 

@app.get("/profile/{user_id}")
async def read_profile(user_id: int):
    try:
        return fetchFromDb(user_id)
        # return JSONResponse(
        #     status_code=status.HTTP_200_OK,
        #     content=profile_data
        # )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Profile not found: {e}")

@app.put("/updateProfile/{user_id}")
async def update_profile(user_id: int, profile: NewProfile):
    try:
        return updateDb(user_id, profile)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'ERROR': str(e)}
        )

@app.delete("/deleteProfile/{user_id}")
async def delete_profile(user_id: int):
    try:
        return deleteFromDb(user_id)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'ERROR': str(e)}
        )

@app.post("/createProfile")
async def create_profile(profile: NewProfile):
    try:
        return storeToDb(profile)
    except Exception as e:
        return JSONResponse(
         status_code=status.HTTP_400_BAD_REQUEST,
         content={'ERROR': str(e)}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8011, log_level="debug", reload=True)
