from config import driver
from selenium.webdriver.common.by import By
from plyer import notification
from get_game_urls import get_game_urls
from get_price import get_price
from save_price import save_price
from check_price_drop import check_price_drop
import logging

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
                notification.notify(
                    title='Alerta de Preço',
                    message=mensagem,
                    app_name='Monitor de Preços',
                    timeout=15
                )

    driver.quit()

if __name__ == '__main__':
    main()
