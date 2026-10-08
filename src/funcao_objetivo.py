# Calcular a FO 

import numpy as np

from logger_config import logger

def calcular_fo_patio(
        matriz_distancias,
        patios_selecionados
): 
    # A ideia é calcular a distância total da solução 
    # Para cada árvore, considera a menor distância até um dos pátios selecionados 

    try:
        # Pegamos os indices dos patios para um array do np
        indices_patios = np.array(
            patios_selecionados,
            dtype= int
        )

        # Selecionamos da matriz de distancias apenas a coluna de patios
        distancias_selecionadas = matriz_distancias[:, indices_patios]

        # Para cada árvore, pegamos a menor distância para um patio escolhido
        menores_distancias = np.min(
            distancias_selecionadas,
            axis = 1
        )

        # Soma as menores distâncias de todas as árvores
        distancia_total = np.sum(
            menores_distancias
        )

        logger.info(
            f"Função objetivo calculada: {distancia_total}"
        )

        return distancia_total

    except Exception as e:
        logger.exception(f"Erro ao calcular a função objetivo: {e}")
        raise

    # Foi feito a distancia dos pátios selecionados 