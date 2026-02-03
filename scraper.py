import asyncio
import os
from playwright.async_api import async_playwright
from supabase import create_client
ù
# Configurazione dai Secrets
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Logica di intercettazione (come nel tuo script originale)
        async def handle_response(response):
            if "vehicles" in response.url and "json" in response.headers.get("content-type", ""):
                data = await response.json()
                raw = data.get("content", data if isinstance(data, list) else [])
                for v in raw:
                    fields = v.get("vehicleStatus", {}).get("dynamicFields", {})
                    if fields.get("latitude"):
                        vehicle_data = {
                            "id": v.get("plate"),
                            "alias": v.get("alias"),
                            "targa": v.get("plate"),
                            "stato": fields.get("vehicleStatus", "N/D"),
                            "lat": float(fields.get("latitude")),
                            "lng": float(fields.get("longitude")),
                            "indirizzo": fields.get("address", "N/D"),
                            "last_update": "now()"
                        }
                        # Salva o aggiorna su Supabase (Upsert)
                        supabase.table("fleet").upsert(vehicle_data).execute()

        page.on("response", handle_response)
        await page.goto("https://macnil.gtfleet.net/")
        await page.fill("#username-field", os.environ.get("MACNIL_USER"))
        await page.fill("#password-field", os.environ.get("MACNIL_PASS"))
        await page.keyboard.press("Enter")
        await page.wait_for_url("**/dashboard/**")
        await page.goto("https://macnil.gtfleet.net/dashboard/vehicles?size=100")
        await asyncio.sleep(10) # Tempo per catturare i dati
        await browser.close()

asyncio.run(run())
