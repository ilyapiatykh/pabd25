import joblib
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from loguru import logger
from pydantic import BaseModel, ValidationError, field_validator


class Apartment(BaseModel):
    total_meters: int
    rooms_count: int
    floors_count: int
    floor: int

    @field_validator("total_meters", "rooms_count", "floors_count", "floor", mode="after")
    @classmethod
    def is_positive(cls, value: int):
        if value < 1:
            raise ValueError("Must be more than 0")

        return value

    def to_df(self):
        return pd.DataFrame(
            [
                {
                    "total_meters": self.total_meters,
                    "rooms_count": self.rooms_count,
                    "floors_count": self.floors_count,
                    "floor": self.floor,
                }
            ]
        )


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

    pred = model.predict(apartment.to_df())

    return JSONResponse(content={"price": int(pred[0])}, status_code=200)
