import asyncio
import os
import requests
from datetime import datetime, timedelta

# 1. URL do seu Proxy na Vercel
URL_PROXY = "https://proxy-blaze-5m7o.vercel.app/api/blaze"

# 2. URL do seu Google Apps Script (Webhook)
URL_WEBHOOK = os.getenv("WEBHOOK_URL", "COLE_AQUI_A_URL_DO_SEU_GOOGLE_APPS_SCRIPT")

# Conjunto para evitar registros duplicados
horarios_enviados = set()

def monitorar_rodadas():
    global horarios_enviados
    try:
        # Consulta o Proxy na Vercel
        response = requests.get(URL_PROXY, timeout=8)
        
        if response.status_code == 200:
            dados = response.json()
            
            if isinstance(dados, list) and len(dados) > 0:
                for item in dados:
                    color = item.get("color")
                    created_at = item.get("created_at")
                    
                    # No Double da Blaze: color == 0 é a Pedra Branca (14x)
                    if color == 0 and created_at:
                        # Converte a data UTC para Horário de Brasília (UTC-3)
                        dt_utc = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                        dt_brt = dt_utc - timedelta(hours=3)
                        horario_br = dt_brt.strftime("%H:%M")
                        
                        # Se ainda não enviamos essa pedra branca
                        if horario_br not in horarios_enviados:
                            horarios_enviados.add(horario_br)
                            print(f"⚪ PEDRA BRANCA CAPTURADA: {horario_br}")

                            # Envio para o Google Apps Script
                            if "script.google.com" in URL_WEBHOOK:
                                try:
                                    payload = {"horario": horario_br}
                                    res = requests.post(URL_WEBHOOK, json=payload, timeout=10)
                                    print(f"✅ Enviado ao Google Apps Script! Resposta: {res.status_code}")
                                except Exception as err:
                                    print(f"❌ Erro ao enviar para o Webhook: {err}")
                            else:
                                print("⚠️ Cole a URL do Google Apps Script na variável URL_WEBHOOK no main.py!")
        else:
            print(f"⚠️ Resposta do Proxy: Status {response.status_code}")

    except Exception as e:
        print(f"Aviso de leitura: {e}")

async def main():
    print("🚀 Robô de Monitoramento Base44/Blaze Iniciado!")
    while True:
        monitorar_rodadas()
        # Verifica novas rodadas a cada 5 segundos (tempo do giro da Blaze)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
