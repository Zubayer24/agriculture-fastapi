from fastapi import FastAPI

from app.endpoints.farms import router as farms_router
from app.endpoints.crops import router as crops_router
#from app.endpoints.markets import router as markets_router

app = FastAPI(title="Agriculture Analytics API")

app.include_router(farms_router)

app.include_router(crops_router)

#app.include_router(markets_router)

