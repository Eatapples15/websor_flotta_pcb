from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os

app = FastAPI()

@app.get("/fleet.geojson")
async def get_geojson():
    return JSONResponse(content={"status": "API connessa", "info": "Se vedi questo, il routing funziona"})

@app.get("/")
async def root():
    return {"message": "Server attivo"}
