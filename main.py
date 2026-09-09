import asyncio
import os
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from playwright.async_api import async_playwright

# Servidor dummy para evitar spin down em Web Service do Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot TipMiner Ativo!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# Insira o link do seu Google Apps Script diretamente aqui ou use variável no Render
URL_WEBHOOK = os.getenv("WEBHOOK_URL", "COLE_AQUI_A_URL_DO_SEU_GOOGLE_APPS_SCRIPT")

horarios_enviados = set()

async def main():
    global horarios_enviados
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("Iniciando monitoramento continuo no TipMiner...")

        while True:
            try:
                # Recarrega a pagina para capturar os dados mais recentes do grid
                await page.goto("https://www.tipminer.com/br/cassinos/blaze/double", wait_until="domcontentloaded", timeout=45000)
                await asyncio.sleep(3)  # Aguarda a renderização dos componentes

                # Busca as células do grid
                cards = await page.query_selector_all("div.cell, div.result-item, div[class*='cell']")
                
                for card in cards:
                    html_content = await card.inner_html()
                    
                    # Filtra os marcadores de pedra branca
                    if "white" in html_content.lower() or "branca" in html_content.lower() or "0.png" in html_content:
                        texto = await card.inner_text()
                        linhas = texto.split("\n")
                        for linha in linhas:
                            linha = linha.strip()
                            if len(linha) == 5 and ":" in linha:
                                if linha not in horarios_enviados:
                                    horarios_enviados.add(linha)
                                    print(f"⚪ PEDRA BRANCA DETECTADA: {linha}")
                                    
                                    if "script.google.com" in URL_WEBHOOK:
                                        try:
                                            res = requests.post(URL_WEBHOOK, json={"horario": linha}, timeout=10)
                                            print(f"✅ Enviado com sucesso ao Google Apps Script! Status: {res.status_code}")
                                        except Exception as err:
                                            print(f"❌ Erro de conexao com Webhook: {err}")
                                    else:
                                        print("⚠️ URL do Webhook nao foi configurada corretamente!")
            except Exception as e:
                print(f"Aviso na execucao do ciclo: {e}")

            # Intervalo de 20 segundos entre verificações de grade
            await asyncio.sleep(20)

if __name__ == "__main__":
    asyncio.run(main())
    import asyncio
import os
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from playwright.async_api import async_playwright

# Servidor de manutenção para evitar o encerramento do Web Service no Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot TipMiner Ativo!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# Configuração do Webhook do Google Apps Script
URL_WEBHOOK = os.getenv("WEBHOOK_URL", "SUA_URL_DO_GOOGLE_APPS_SCRIPT_AQUI")

horarios_enviados = set()

async def main():
    global horarios_enviados
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("Conectando ao TipMiner Double Blaze...")
        await page.goto("https://www.tipminer.com/br/cassinos/blaze/double", wait_until="domcontentloaded", timeout=60000)

        while True:
            try:
                # Busca os blocos de resultados no TipMiner
                cards = await page.query_selector_all("div.cell, div.result-item, div[class*='cell']")
                
                for card in cards:
                    html_content = await card.inner_html()
                    # Identifica se a célula corresponde à pedra branca
                    if "white" in html_content.lower() or "branca" in html_content.lower() or "0.png" in html_content:
                        texto = await card.inner_text()
                        linhas = texto.split("\n")
                        for linha in linhas:
                            linha = linha.strip()
                            # Procura pelo formato de horário HH:MM
                            if len(linha) == 5 and ":" in linha:
                                if linha not in horarios_enviados:
                                    horarios_enviados.add(linha)
                                    print(f"⚪ PEDRA BRANCA ENCONTRADA: {linha}")
                                    
                                    try:
                                        res = requests.post(URL_WEBHOOK, json={"horario": linha}, timeout=10)
                                        print(f"✅ Enviado ao Google Sites! Resposta: {res.status_code}")
                                    except Exception as err:
                                        print(f"❌ Erro ao enviar Webhook: {err}")
            except Exception as e:
                print(f"Aviso de leitura: {e}")

            # Aguarda 15 segundos para a próxima varredura
            await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(main())
    import asyncio
import os
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from playwright.async_api import async_playwright

# Servidor de manutenção de porta para o Render Web Service
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot TipMiner Ativo!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# Configuração do Webhook do Google Apps Script
URL_WEBHOOK = os.getenv("WEBHOOK_URL", "SUA_URL_DO_GOOGLE_APPS_SCRIPT_AQUI")

ultimo_horario_enviado = ""

async def main():
    global ultimo_horario_enviado
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("Conectando ao TipMiner Double Blaze...")
        await page.goto("https://www.tipminer.com/br/cassinos/blaze/double", wait_until="domcontentloaded")

        while True:
            try:
                # Procura no HTML por pedras brancas (ícones de fogo/diamante branco ou estilo branco)
                # O TipMiner exibe cada rodada com classes específicas para pedras brancas
                elementos_brancos = await page.query_selector_all('.white, [class*="white"], [data-color="white"]')
                
                for el in elementos_brancos:
                    # Tenta capturar o texto do horário abaixo da pedra
                    texto = await el.inner_text()
                    if ":" in texto:
                        horario = texto.strip()
                        
                        # Evita enviar o mesmo horário repetidamente
                        if horario != ultimo_horario_enviado:
                            ultimo_horario_enviado = horario
                            print(f"⚪ PEDRA BRANCA ENCONTRADA no TipMiner às {horario}!")
                            
                            # Envia para o Google Apps Script
                            try:
                                requests.post(URL_WEBHOOK, json={"horario": horario}, timeout=10)
                                print("✅ Enviado com sucesso para o Google Sites!")
                            except Exception as err:
                                print(f"❌ Erro de envio ao Webhook: {err}")
                            break
            except Exception as e:
                pass

            # Aguarda 10 segundos antes de verificar novamente
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
    import asyncio
import os
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from playwright.async_api import async_playwright
from datetime import datetime

# Servidor Falso para enganar a checagem de porta do Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot esta rodando!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Inicia o servidor em uma thread separada
threading.Thread(target=run_dummy_server, daemon=True).start()

# --- DAQUI PARA BAIXO SEGUE O SEU CÓDIGO NORMAL ---
URL_WEBHOOK = os.getenv("WEBHOOK_URL", "SUA_URL_DO_GOOGLE_APPS_SCRIPT_AQUI")

async def handle_response(response):
    if "roulette_games/recent" in response.url and response.status == 200:
        try:
            data = await response.json()
            for item in data:
                color_id = item.get("color")
                created_at = item.get("created_at")
                
                if color_id == 0 and created_at:
                    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    hora_formatada = dt.strftime("%H:%M")

                    print(f"⚪ BRANCO DETECTADO às {hora_formatada}!")

                    try:
                        requests.post(URL_WEBHOOK, json={"horario": hora_formatada}, timeout=10)
                        print("✅ Enviado para o Google Sites!")
                    except Exception as req_err:
                        print(f"❌ Erro ao enviar: {req_err}")
        except Exception:
            pass

async def main():
    async with async_playwright() as p:
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
