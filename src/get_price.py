import requests
from bs4 import BeautifulSoup
import logging
from src.config import HEADERS

def get_price(game_url):
    """ Gets the price of a game from its url. """
    try:
        response = requests.get(game_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Captura o país
        first_country = soup.select('body > div.wrapper.main-wrapper > div.well > table > tbody > tr:nth-child(1) > td:nth-child(2)')[0].get_text().strip()
        second_country = soup.select('body > div.wrapper.main-wrapper > div.well > table > tbody > tr:nth-child(2) > td:nth-child(2)')[0].get_text().strip()
        third_country = soup.select('body > div.wrapper.main-wrapper > div.well > table > tbody > tr:nth-child(3) > td:nth-child(2)')[0].get_text().strip()
        country = first_country

        # Captura o preço
        element = soup.find('td', class_="price-value")
        discount = element.find('div', class_="discounted")

        # Tira Argentina da jogada já que não podemos comprar la
        if "Argentina" in first_country or "Driffle" in first_country or "Eneba" in first_country and discount:
            price_list = soup.find_all('del', limit=2)
            original_price = price_list[1]
            country = second_country
        elif "Argentina" in first_country or "Driffle" in first_country or "Eneba" in first_country and not discount:
            original_price = soup.find('del')
            country = second_country
        else:
            original_price = soup.find('del')

        if "Driffle" in country or "Eneba" in country:
            country = third_country

        if original_price:
            discounted_price = original_price.find_next_sibling(string=True)
            if discounted_price:
                price = discounted_price.strip()
                # Retorna price e pais como um tupla
                return ''.join(filter(lambda x: x.isdigit() or x in ',.', price)), country
        return None, None # Se não encontrar preço, retorna None para ambos
    except Exception as e:
        logging.error(f'Erro ao obter preço: {e}')
        return None
