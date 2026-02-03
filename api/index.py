from fastapi import FastAPI
from fastapi.responses import JSONResponse
from supabase import create_client
import os

app = FastAPI()

# Leggiamo le variabili d'ambiente
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

@app.get("/fleet.geojson")
async def get_geojson():
    try:
        # Controllo di sicurezza: se le chiavi mancano, diamo un errore chiaro invece di crashare
        if not SUPABASE_URL or not SUPABASE_KEY:
            return JSONResponse(
                content={"error": "Configurazione mancante: SUPABASE_URL o SUPABASE_KEY non trovate su Vercel."}, 
                status_code=500
            )

        # Inizializziamo il client qui per sicurezza
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Recupero dati
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
    return {
        "status": "online", 
        "database_env_present": SUPABASE_URL is not None and SUPABASE_KEY is not None
    }
