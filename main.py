# main.py existente — isso é um problema herdado?
from fastapi import FastAPI
from api.pricing_execution_controller import router as pricing_execution_router
from api.structures_controller import router as structures_router


app = FastAPI()
app.include_router(pricing_execution_router)
app.include_router(structures_router)
