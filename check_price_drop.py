import os
import pandas as pd
import logging
from config import PASTA_HISTORICO

def check_price_drop(game_name):
    """ Verifica se houve queda de preço. """
    try:
        history_file = os.path.join(PASTA_HISTORICO, f'{game_name}_price_history.csv')

        if not os.path.exists(history_file):
            logging.warning(f'Arquivo de histórico não encontrado para {game_name}.')
            return False

        historico = pd.read_csv(history_file)

        if len(historico) < 2:
            return False

        historico['preco'] = historico['preco'].astype(str).str.replace(',', '.').astype(float)
        preco_atual = historico.iloc[-1]['preco']
        menor_preco_anterior = historico['preco'].iloc[:-1].min()

        logging.info(f"Preço atual: {preco_atual}, Menor preço anterior: {menor_preco_anterior}")

        return preco_atual < menor_preco_anterior
    except Exception as e:
        logging.error(f'Erro na verificação: {e}')
        return False
