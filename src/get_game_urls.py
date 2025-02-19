from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.config import driver, BASE_URL
import logging


def get_game_urls():
    """ Captura as URLs dos jogos em todas as páginas disponíveis. """
    game_urls = []
    page_number = 1  # Começa na página 1

    while True:
        url_pagina = f"{BASE_URL}&page={page_number}"  # URL da página atual
        driver.get(url_pagina)

        try:
            # Espera até que os jogos carreguem
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "games-list-item"))
            )

            # Coleta os links dos jogos
            game_links = driver.find_elements(By.XPATH, '//a[@class="games-list-item"]')
            urls_pagina = [link.get_attribute("href") for link in game_links]

            if not urls_pagina:
                break  # Sai do loop se não houver mais jogos

            game_urls.extend(urls_pagina)
            logging.info(f"Página {page_number} capturada com {len(urls_pagina)} jogos.")

            page_number += 1  # Avança para a próxima página

        except Exception as e:
            logging.error(f"Erro ao capturar jogos da página {page_number}: {e}")
            break  # Sai do loop em caso de erro

    return game_urls
