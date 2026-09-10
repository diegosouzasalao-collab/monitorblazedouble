import asyncio
import os
import requests
from datetime import datetime, timedelta

# URL do seu proxy criado na Vercel
URL_PROXY = "https://proxy-blaze-5m7o.vercel.app/api/blaze"

# URL do seu Google Apps Script (Webhook)
URL_WEBHOOK = os.getenv("https://script.google.com/macros/s/AKfycbzU_ZsBTQFIg4vtTjMbf64brp6U2mW0wh7AnT7dWOGPi6hopZYCpwzBJ9fPwFv7BhMi/exec")

horarios_enviados = set()

def monitorar_com_proxy():
    global horarios_enviados
    try:
        response = requests.get(URL_PROXY, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            
            if isinstance(dados, list):
                for item in dados:
                    color = item.get("color")
                    created_at = item.get("created_at")
                    
                    # color == 0 representa a Pedra Branca
                    if color == 0 and created_at:
                        # Converte de UTC para Horário de Brasília (UTC-3)
                        dt_utc = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                        dt_brt = dt_utc - timedelta(hours=3)
                        horario_formatado = dt_brt.strftime("%H:%M")
                        
                        if horario_formatado not in horarios_enviados:
                            horarios_enviados.add(horario_formatado)
                            print(f"⚪ PEDRA BRANCA CAPTURADA: {horario_formatado}")

                            if "script.google.com" in URL_WEBHOOK:
                                try:
                                    res = requests.post(URL_WEBHOOK, json={"horario": horario_formatado}, timeout=10)
                                    print(f"✅ Enviado ao Google Apps Script! Status: {res.status_code}")
                                except Exception as err:
                                    print(f"❌ Erro de envio ao Webhook: {err}")
    except Exception as e:
        print(f"Aviso de consulta: {e}")

async def main():
    print("🚀 Robô ativado e conectado ao Proxy da Vercel!")
    while True:
        monitorar_com_proxy()
        await asyncio.sleep(8)

if __name__ == "__main__":
    asyncio.run(main())
