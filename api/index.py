from fastapi import FastAPI
from fastapi.responses import JSONResponse
from supabase import create_client
import os

app = FastAPI()

# Inizializzazione client Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.get("/fleet.geojson")
async def get_geojson():
    try:
        # Recupera i dati dalla tabella
        res = supabase.table("fleet").select("*").execute()
        
        features = []
        for v in res.data:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point", 
                    "coordinates": [float(v["lng"]), float(v["lat"])]
                },
                "properties": v
            })
        
        return JSONResponse(content={
            "type": "FeatureCollection", 
            "features": features
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Rotta di test per vedere se l'API risponde
@app.get("/")
async def root():
    return {"status": "running", "database_connected": url is not None}
