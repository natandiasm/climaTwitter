import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

from .routers.v1 import core
# Import Routers

from .utils.openweathermap import OpenWeatherMap
from .utils.twitter import Twitter

# Load env file
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start OpenWeatherMap
    owm = OpenWeatherMap()
    owm.start()

    # Start Twitter
    twt = Twitter()
    twt.start()
    yield


# Create instance of FastAPI
app = FastAPI(title="climaTwitter",
              description="an application that consumes the openweathermap and twitter api, connecting them into a "
                          "simple to use and fast api.",
              summary="tweet a city's current weather.",
              docs_url="/doc",
              version=os.getenv("VERSION"),
              lifespan=lifespan
              )

# Import the routes that make up version 1
app.include_router(core.router, prefix='/v1')


@app.get("/", description="main endpoint, with it you will know if the api is up and what the api version is.")
async def root():
    return {"name": "ClimaTwitter", "version": os.getenv("VERSION")}
