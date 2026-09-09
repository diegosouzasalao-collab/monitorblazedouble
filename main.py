import asyncio
import os
import requests
from datetime import datetime, timedelta

# Insira a URL do seu Google Apps Script diretamente aqui ou configure no Render (WEBHOOK_URL)
URL_WEBHOOK = os.getenv("WEBHOOK_URL", "COLE_AQUI_A_URL_DO_SEU_GOOGLE_APPS_SCRIPT")

horarios_enviados = set()

def buscar_resultados():
    global horarios_enviados
    
    # Usa um proxy público para mascarar o IP do Render e burlar o Cloudflare
    url_proxy = "https://api.allorigins.win/get?url=" + requests.utils.quote("https://blaze.com/api/roulette_games/recent")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url_proxy, headers=headers, timeout=12)
        
        if response.status_code == 200:
            data = response.json()
            # Extrai o conteúdo brutos da API enviado pelo proxy
            import json
            conteudo = json.loads(data.get("contents", "[]"))
            
            for item in conteudo:
                color = item.get("color")
                created_at = item.get("created_at")
                
                # color == 0 representa a Pedra Branca
                if color == 0 and created_at:
                    # Converte de UTC para Horário Oficial de Brasília (UTC-3)
                    dt_utc = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    dt_brt = dt_utc - timedelta(hours=3)
                    horario_formatado = dt_brt.strftime("%H:%M")
                    
                    if horario_formatado not in horarios_enviados:
                        horarios_enviados.add(horario_formatado)
                        print(f"⚪ PEDRA BRANCA ENCONTRADA: {horario_formatado}")

                        # Envio ao Google Apps Script
                        if "script.google.com" in URL_WEBHOOK:
                            try:
                                res = requests.post(URL_WEBHOOK, json={"horario": horario_formatado}, timeout=10)
                                print(f"✅ Enviado ao Google Apps Script! Status: {res.status_code}")
                            except Exception as err:
                                print(f"❌ Erro de conexao Webhook: {err}")
                        else:
                            print("⚠️ ATENÇÃO: Adicione a URL do Google Apps Script na variável URL_WEBHOOK!")
        else:
            print(f"⚠️ Servidor proxy respondeu com status: {response.status_code}")

    except Exception as e:
        print(f"Aviso no ciclo de consulta: {e}")

async def main():
    print("🚀 Monitoramento via Proxy iniciado com sucesso!")
    while True:
        buscar_resultados()
        # Consulta a cada 10 segundos
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
