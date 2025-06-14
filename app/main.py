from contextlib import asynccontextmanager

import joblib
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from app.config import Config
from app.handlers import router
from app.s3 import S3Client


def create_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):

        config = Config.model_validate({})
        app.state.config = config

        s3 = S3Client(config)
        s3.download_model()

        model = joblib.load("../models/model.pkl")
        app.state.model = model

        templates = Jinja2Templates(directory="templates")
        app.state.templates = templates

        yield

    app = FastAPI(lifespan=lifespan)

    app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    return app


def main():
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
