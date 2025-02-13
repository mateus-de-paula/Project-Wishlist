import requests
from bs4 import BeautifulSoup
import logging
from config import HEADERS

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
