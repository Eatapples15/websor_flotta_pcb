from fastapi import FastAPI
from fastapi.responses import JSONResponse
from supabase import create_client
import os

app = FastAPI()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

@app.get("/fleet.geojson")
async def get_geojson():
    res = supabase.table("fleet").select("*").execute()
    features = []
    for v in res.data:
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [v["lng"], v["lat"]]},
            "properties": v
        })
    return JSONResponse(content={"type": "FeatureCollection", "features": features})
