from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from loguru import logger
from pydantic import ValidationError

from app.models import Apartment

router = APIRouter(tags=["apartment_pricing"])


async def verify_auth(request: Request, authorization: str = Header(..., alias="Authorization")):
    if authorization != request.app.state.config.jwt_token.get_secret_value():
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/", response_class=HTMLResponse, summary="Main page")
async def index(request: Request):
    return request.app.state.templates.TemplateResponse("index.html", {"request": request})


@router.post("/api/numbers", summary="Predict apartment price")
async def process_numbers(request: Request, _: Annotated[None, Depends(verify_auth)]):
    try:
        data = await request.json()
        apartment = Apartment.model_validate(data)

        prediction = request.app.state.model.predict(apartment.to_df())

        return JSONResponse(content={"price": int(prediction[0])})

    except ValidationError as e:
        logger.warning(f"Invalid input data: {data}")
        raise HTTPException(422, detail=e.errors())

    except Exception as e:
        logger.exception("Prediction failed")
        raise e
