import asyncio
import os
import requests

# Subsitua pelo link do seu Google Apps Script se não usar a variável do Render
URL_WEBHOOK = os.getenv("WEBHOOK_URL", "COLE_AQUI_A_URL_DO_SEU_GOOGLE_APPS_SCRIPT")

horarios_enviados = set()

def buscar_resultados_api():
    global horarios_enviados
    url_api = "https://blaze.com/api/roulette_games/recent"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url_api, headers=headers, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            for item in dados:
                color = item.get("color")
                created_at = item.get("created_at")
                
                # color == 0 representa a Pedra Branca
                if color == 0 and created_at:
                    # Extrai o horário (HH:MM) a partir do horário UTC da API
                    horario = created_at.split("T")[1][:5]
                    
                    if horario not in horarios_enviados:
                        horarios_enviados.add(horario)
                        print(f"⚪ PEDRA BRANCA DETECTADA VIA API: {horario}")

                        if "script.google.com" in URL_WEBHOOK:
                            try:
                                res = requests.post(URL_WEBHOOK, json={"horario": horario}, timeout=10)
                                print(f"✅ Enviado ao Google Apps Script! Status: {res.status_code}")
                            except Exception as err:
                                print(f"❌ Erro ao enviar para o Webhook: {err}")
                        else:
                            print("⚠️ URL_WEBHOOK não configurada corretamente!")
    except Exception as e:
        print(f"Aviso de leitura da API: {e}")

async def main():
    print("🚀 Bot leve iniciado! Monitorando API da Blaze...")
    while True:
        buscar_resultados_api()
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
