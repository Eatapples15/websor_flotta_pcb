from fastapi import FastAPI
from fastapi.responses import JSONResponse
from supabase import create_client
import os

app = FastAPI()

# Inizializzazione client Supabase utilizzando le variabili d'ambiente di Vercel
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.get("/fleet.geojson")
async def get_geojson():
    try:
        # Recupera tutti i dati dalla tabella 'fleet'
        res = supabase.table("fleet").select("*").execute()
        
        features = []
        for v in res.data:
            # Creiamo la struttura GeoJSON standard
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point", 
                    "coordinates": [float(v["lng"]), float(v["lat"])]
                },
                "properties": {
                    "alias": v.get("alias"),
                    "targa": v.get("targa"),
                    "stato": v.get("stato"),
                    "indirizzo": v.get("indirizzo"),
                    "ultimo_aggiornamento": v.get("last_update")
                }
            })
        
        return JSONResponse(content={
            "type": "FeatureCollection",
            "features": features
        })
    except Exception as e:
        # In caso di errore (es. tabelle mancanti o chiavi errate)
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
async def root():
    return {
        "status": "online", 
        "database_connected": url is not None,
        "endpoint": "/fleet.geojson"
    }
