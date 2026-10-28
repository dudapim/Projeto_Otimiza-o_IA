# Calcular a FO 

import numpy as np
from logger_config import logger
from modelos.solucao import Solucao  

def calcular_fo_patio(
        matriz_distancias,
        patios_selecionados,
        volumes_arvores,
        distancia_maxima,
        penalizacao_volume,
        rest_vol_sup
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

        # Procura o índice da menor distância em cda linha
        indices_patio_mais_proximo = np.argmin(
            distancias_selecionadas,
            axis= 1
        )

        #Percorrendo todas as árvores de forma vetorizada
        volumes_por_patio = np.bincount(
            indices_patio_mais_proximo,
            weights = volumes_arvores,
            minlength = len(patios_selecionados)
        )

        # Soma as menores distâncias de todas as árvores
        distancia_total = np.sum(
            menores_distancias
        )

        # A penalização de distância
        # O maximum faz o calculo de excessão para todas as árvores
        # Se der positivo, existe excesso
        # Se der negativo, não há excesso, então usamos 0
        diferenca_distancia = np.sum(
            np.maximum(
                menores_distancias - distancia_maxima,
                0
            )
        )

        # A penalização do volume
        # Calculo do excesso de volume, para descobrir quanto de volume está sobrando acima do limite permitido em cada pátio
        diferenca_volume = np.sum(
            np.maximum(
                volumes_por_patio - rest_vol_sup,
                0
            )
        )

        # A penalização final
        penalizacao = penalizacao_volume * (
            diferenca_volume + diferenca_distancia
        )

        distancia_total += penalizacao

        #Verifica a viabilidade, só é verdadeira se não houver penalizações
        viavel = (diferenca_volume + diferenca_distancia) == 0

        solucao_gerada = Solucao(
            patios_selecionados=patios_selecionados,
            distancia_total=distancia_total,
            viavel=viavel
        )

        logger.info(
            f"Função objetivo calculada: {distancia_total}"
        )
        
        return solucao_gerada

    except Exception as e:
        logger.exception(f"Erro ao calcular a função objetivo: {e}")
        raise

    # Foi feito a distancia dos pátios selecionados 


