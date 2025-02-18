import os
import pandas as pd
import logging
from src.config import PASTA_HISTORICO

def check_price_drop(game_name):
    """ Verifica se houve queda de preço. """
    try:
        history_file = os.path.join(PASTA_HISTORICO, f'{game_name}_price_history.csv')

        if not os.path.exists(history_file):
            logging.warning(f'Arquivo de histórico não encontrado para {game_name}.')
            return False

        history = pd.read_csv(history_file)

        if len(history) < 2:
            return False

        history['price'] = history['price'].astype(str).str.replace(',', '.').astype(float)
        current_price = history.iloc[-1]['price']
        lowest_previous_price = history['price'].iloc[:-1].min()

        logging.info(f"Preço atual: {current_price}, Menor preço anterior: {lowest_previous_price}")

        return current_price < lowest_previous_price
    except Exception as e:
        logging.error(f'Erro na verificação: {e}')
        return False
