from src.config import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from plyer import notification
from src.get_game_urls import get_game_urls
from src.get_price import get_price
from src.save_price import save_price
from src. check_price_drop import check_price_drop
import logging
import time
import random

def main():
    '''
    This is the main file. It calls the other functions, gets the games' names and also sends alerts in case there's a
    price drop.
    :return:
    '''
    game_urls = get_game_urls()

    for game_url in game_urls:
        # Intervalo aleatório entre 3 a 7 segundos
        time.sleep(random.uniform(3, 7))
        driver.get(game_url)
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.mt8.lc3.lcm2'))
            )
            game_name = elemento.text.replace(":", "").replace("®", "").replace("™","")
        except:
            print("Elemento não encontrado.")

        logging.info(f"Verificando {game_name}...")

        price, country = get_price(game_url)

        if price:
            logging.info(f"Preço de {game_name}: {price} ({country})")
            save_price(price, game_name, country)
            if check_price_drop(game_name):
                msg = f'⚠️ QUEDA DETECTADA! ⚠️\n{game_name}\nNovo preço: R${price} ({country})'
                notification.notify(
                    title='Alerta de Preço',
                    message=msg,
                    app_name='Monitor de Preços',
                    timeout=15
                )

    driver.quit()

if __name__ == '__main__':
    main()
