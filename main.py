import os
import logging
import requests
import pandas as pd
from datetime import datetime
#from plyer import notification
from win10toast import ToastNotifier
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

#Criando logs (mensagens)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='log_de_execução.log')

load_dotenv()

CHROME_PROFILE_PATH = os.getenv('CHROME_PROFILE_PATH')
BASE_URL = os.getenv('BASE_URL', "https://eshop-prices.com/wishlist?currency=BRL&sort_by=discount&direction=desc")
if not CHROME_PROFILE_PATH:
    raise ValueError("Caminho do perfil do Chrome não definido. Configure o arquivo .env.")

#Pasta onde as planilhas serão criadas
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
driver.minimize_window()  # Minimiza a janela do navegador
#driver.set_window_position(-10000, 0) # Isso move a janela para fora da área visível, sem fechá-la.

def get_game_urls():
    """ Captura as URLs dos jogos na página principal. """
    driver.get(BASE_URL)

    # Espera até os jogos aparecerem na tela
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "games-list-item"))
    )

    game_links = driver.find_elements(By.CLASS_NAME, "games-list-item")  # Ajuste o seletor conforme necessário
    game_urls = [link.get_attribute("href") for link in game_links]

    return game_urls


def get_price(game_url):
    """ Captura o preço de um jogo a partir da sua página. """
    try:
        response = requests.get(game_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        original_price = soup.find('del')
        if original_price:
            discounted_price = original_price.find_next_sibling(string=True)
            if discounted_price:
                price = discounted_price.strip()
                return ''.join(filter(lambda x: x.isdigit() or x in ',.', price))
        return None
    except Exception as e:
        logging.error(f'Erro ao obter preço: {e}')
        return None


def save_price(price, game_name):
    """ Salva o preço no histórico. """
    try:
        # Garante que a pasta existe
        if not os.path.exists(PASTA_HISTORICO):
            os.makedirs(PASTA_HISTORICO)

        history_file = os.path.join(PASTA_HISTORICO, f'{game_name}_price_history.csv')

        new_data = pd.DataFrame([{
            'data': datetime.now().strftime('%Y-%m-%d'),
            'preco': price,
            'jogo': game_name
        }])

        # Salva o CSV na pasta definida
        with open(history_file, 'a') as f:
            new_data.to_csv(f, header=f.tell() == 0, index=False)
            logging.info(f'Histórico salvo em: {history_file}')  # Mensagem informativa
    except Exception as e:
        logging.error(f'Erro ao salvar: {e}')


def check_price_drop(game_name):
    """ Verifica se houve queda de preço. """
    try:
        # Define o caminho completo para o arquivo CSV
        history_file = os.path.join(PASTA_HISTORICO, f'{game_name}_price_history.csv')

        # Verifica se o arquivo existe antes de tentar lê-lo
        if not os.path.exists(history_file):
            logging.warning(f'Arquivo de histórico não encontrado para {game_name}.')
            return False

        historico = pd.read_csv(history_file)

        if len(historico) < 2:
            return False

        historico['preco'] = historico['preco'].astype(str).str.replace(',', '.').astype(float)
        preco_atual = historico.iloc[-1]['preco']
        menor_preco_anterior = historico['preco'].iloc[:-1].min()  # Menor preço excluindo o último

        logging.info(f"Preço atual: {preco_atual}, Menor preço anterior: {menor_preco_anterior}")

        return preco_atual < menor_preco_anterior
    except Exception as e:
        logging.error(f'Erro na verificação: {e}')
        return False


def main():
    game_urls = get_game_urls()

    for game_url in game_urls:
        if game_url is None:
            continue
        driver.get(game_url)
        game_name = driver.find_element(By.CSS_SELECTOR, '.mt8.lc3.lcm2').text.replace(":", "").replace("®", "")
        logging.info(f"Verificando {game_name}...")

        price = get_price(game_url)

        if price:
            save_price(price, game_name)
            if check_price_drop(game_name):
                mensagem = f'⚠️ QUEDA DETECTADA! ⚠️\n{game_name}\nNovo preço: R${price}'
                toast = ToastNotifier()
                toast.show_toast(
                    "Alerta de Preço",
                    mensagem,
                    duration=15
                )

    driver.quit()  # Fecha o WebDriver


if __name__ == '__main__':
    main()
