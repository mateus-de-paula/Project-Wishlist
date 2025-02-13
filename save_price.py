import os
import pandas as pd
from datetime import datetime
import logging
from config import PASTA_HISTORICO

def save_price(price, game_name):
    """ Salva o preço no histórico. """
    try:
        if not os.path.exists(PASTA_HISTORICO):
            os.makedirs(PASTA_HISTORICO)

        history_file = os.path.join(PASTA_HISTORICO, f'{game_name}_price_history.csv')

        new_data = pd.DataFrame([{
            'data': datetime.now().strftime('%Y-%m-%d'),
            'preco': price,
            'jogo': game_name
        }])

        with open(history_file, 'a') as f:
            new_data.to_csv(f, header=f.tell() == 0, index=False)
            logging.info(f'Histórico salvo em: {history_file}')
    except Exception as e:
        logging.error(f'Erro ao salvar: {e}')
