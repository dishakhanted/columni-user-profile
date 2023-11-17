from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse("/static/index.html")

class NewProfile(BaseModel):
    user_id: int
    school_id: int
    first_name: str
    last_name: str
    columbiaEmail: str
    password: str
    profilePicture: str  # Consider using Url type
    major: str
    jobTitle: Optional[str] = "NA"
    company: Optional[str] = "NA"
    graduationDate: str
    userDescription: Optional[str] = "NA"
    creationDT: str  # Consider using datetime type

def fetchFromDb(user_id: int):
    # Placeholder for fetching data from the database
    return {
        'user_id': user_id,
        # ... other fields
    }

def updateDb(user_id: int, profile: NewProfile):
    # Placeholder for updating data in the database
    # Ensure the update is for the specific user_id
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=profile.dict()
    )

def deleteFromDb(user_id: int):
    # Placeholder for deleting data from the database
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': f'Profile with user_id {user_id} deleted successfully'}
    )

def storeToDb(profile: NewProfile):
    # Placeholder for storing data in the database
    # Store all profile details, not just first and last name
    return JSONResponse(
         status_code=status.HTTP_200_OK,
         content=profile.dict()
    )

@app.get("/profile/{user_id}")
async def read_profile(user_id: int):
    try:
        profile_data = fetchFromDb(user_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=profile_data
        )
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
    uvicorn.run(app, host="0.0.0.0", port=8011)
