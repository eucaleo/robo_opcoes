# main.py existente — isso é um problema herdado?
from fastapi import FastAPI
from api.pricing_execution_controller import router as pricing_execution_router

app = FastAPI()
app.include_router(pricing_execution_router)

