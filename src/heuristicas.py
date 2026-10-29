import numpy as np
from funcao_objetivo import calcular_fo_patio
from logger_config import logger
from excecoes import DadosInconsistentesError

def obter_solucao_aleatoria(
        todos_indices_patios, 
        qtd_patios_selecionar,
        matriz_distancias,
        volumes_arvores,
        distancia_maxima,
        penalizacao_volume,
        rest_vol_sup
):
    try:
        # Validação de segurança: previne erro se pedirmos mais pátios do que os existentes
        total_disponivel = len(todos_indices_patios)
        if qtd_patios_selecionar > total_disponivel:
            raise DadosInconsistentesError(
                f"Tentativa de selecionar {qtd_patios_selecionar} pátios, "
                f"mas apenas {total_disponivel} estão disponíveis."
            )

        # 1. Seleciona pátios aleatórios sem repetição
        patios_aleatorios = np.random.choice(
            todos_indices_patios, 
            size=qtd_patios_selecionar, 
            replace=False
        ).tolist() 
        
        # 2. Calcula a FO da solução gerada
        solucao = calcular_fo_patio(
            matriz_distancias,
            patios_aleatorios,
            volumes_arvores,
            distancia_maxima,
            penalizacao_volume,
            rest_vol_sup
        )
        
        # Pode adicionar um log de debug se quiser acompanhar os sorteios
        logger.debug(f"Solução aleatória gerada com sucesso. Pátios: {patios_aleatorios}")
        
        return solucao

    except DadosInconsistentesError as e:
        # Se for o nosso erro de validação, apenas regista e sobe a exceção
        logger.error(f"Erro de consistência ao gerar solução aleatória: {e}")
        raise
    except Exception as e:
        # Se for um erro inesperado (ex: matriz de distâncias com formato errado)
        logger.exception(f"Erro inesperado ao gerar solução aleatória: {e}")
        raise