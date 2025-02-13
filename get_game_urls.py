from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import driver, BASE_URL

def get_game_urls():
    """ Captura as URLs dos jogos na página principal. """
    driver.get(BASE_URL)

    # Espera até os jogos aparecerem na tela
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "games-list-item"))
    )

    game_links = driver.find_elements(By.CLASS_NAME, "games-list-item")
    game_urls = [link.get_attribute("href") for link in game_links]

    return game_urls
