from src.config import driver
from selenium.webdriver.common.by import By
from plyer import notification
from src.get_game_urls import get_game_urls
from src.get_price import get_price
from src.save_price import save_price
from src. check_price_drop import check_price_drop
import logging

def main():
    game_urls = get_game_urls()

    for game_url in game_urls:
        if game_url is None:
            continue
        driver.get(game_url)
        game_name = driver.find_element(By.CSS_SELECTOR, '.mt8.lc3.lcm2').text.replace(":", "").replace("®", "")
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
