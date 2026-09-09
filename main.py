import asyncio
import os
import requests
from playwright.async_api import async_playwright
from datetime import datetime

# Substitua pela URL do seu Google Apps Script
URL_WEBHOOK = os.getenv("WEBHOOK_URL", "SUA_URL_DO_GOOGLE_APPS_SCRIPT_AQUI")

async def handle_response(response):
    if "roulette_games/recent" in response.url and response.status == 200:
        try:
            data = await response.json()
            for item in data:
                color_id = item.get("color")
                created_at = item.get("created_at")
                
                # Se for Pedra Branca (color_id == 0)
                if color_id == 0 and created_at:
                    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    hora_formatada = dt.strftime("%H:%M")

                    print(f"⚪ BRANCO DETECTADO às {hora_formatada}!")

                    # Envia para o Google Apps Script
                    try:
                        requests.post(URL_WEBHOOK, json={"horario": hora_formatada}, timeout=10)
                        print("✅ Enviado para o Google Sites!")
                    except Exception as req_err:
                        print(f"❌ Erro ao enviar: {req_err}")
        except Exception:
            pass

async def main():
    async with async_playwright() as p:
        # No Render precisa rodar sem interface gráfica (headless=True)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        page.on("response", handle_response)

        print("Conectado à Blaze na Nuvem...")
        await page.goto("https://blaze.com/pt/games/double", wait_until="domcontentloaded")

        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())