# main.py
from fastapi import FastAPI

from api.pricing_execution_controller import router as pricing_execution_router
from api.structures_controller import router as structures_router

app = FastAPI(
    title="Structures API",
    version="0.1.0",
)

app.include_router(pricing_execution_router)
app.include_router(structures_router)
