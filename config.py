import os
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Carrega as variáveis de ambiente
load_dotenv()

# Caminho do perfil do Chrome
CHROME_PROFILE_PATH = os.getenv('CHROME_PROFILE_PATH')
BASE_URL = os.getenv('BASE_URL', "https://eshop-prices.com/wishlist?currency=BRL&sort_by=discount&direction=desc")
if not CHROME_PROFILE_PATH:
    raise ValueError("Caminho do perfil do Chrome não definido. Configure o arquivo .env.")

# Pasta para salvar histórico de preços
PASTA_HISTORICO = 'historico_precos'

# Configuração do Selenium
options = webdriver.ChromeOptions()
options.add_argument(f'user-data-dir={CHROME_PROFILE_PATH}')
options.add_argument("--no-sandbox")

# Configurações do Requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Inicializa o WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.minimize_window()

# Configuração de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='log_de_execução.log')
