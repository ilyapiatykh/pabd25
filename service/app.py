import joblib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from loguru import logger
from pydantic import BaseModel, ValidationError, field_validator


class Apartment(BaseModel):
    area: int
    num_rooms: int
    total_floors: int
    floor: int

    @field_validator('area', 'num_rooms', 'total_floors', 'floor', mode='after')
    @classmethod
    def is_positive(cls, value: int):
        if value < 1:
            raise ValueError("Must be more than 0")

        return value


app = FastAPI()

templates = Jinja2Templates(directory="templates")

model = joblib.load("../models/model.pkl")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/numbers")
@logger.catch(Exception, message="Failed to predict apartment price")
async def process_numbers(request: Request):
    data = await request.json()

    try:
        apartment = Apartment.model_validate(data)
    except ValidationError as e:
        logger.warning("Failed to validate input data")
        return JSONResponse(content=e.errors(), status_code=422)

    pred = model.predict([[apartment.area, apartment.num_rooms, apartment.total_floors, apartment.floor]])

    return JSONResponse(content={"price": pred[0]}, status_code=200)
