from fastapi import FastAPI
from fastapi.responses import JSONResponse
from supabase import create_client
import os

app = FastAPI()

# Recupero variabili d'ambiente
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

@app.get("/fleet.geojson")
async def get_geojson():
    try:
        # Verifichiamo che le chiavi esistano
        if not url or not key:
            return JSONResponse(content={"error": "Chiavi Supabase mancanti nei Settings di Vercel"}, status_code=500)
        
        # Inizializziamo il client dentro la funzione per evitare crash all'avvio
        supabase = create_client(url, key)
        res = supabase.table("fleet").select("*").execute()
        
        features = []
        for v in res.data:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point", 
                    "coordinates": [float(v.get("lng", 0)), float(v.get("lat", 0))]
                },
                "properties": v
            })
        
        return JSONResponse(content={"type": "FeatureCollection", "features": features})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
async def root():
    return {"status": "online", "config_ok": url is not None}
