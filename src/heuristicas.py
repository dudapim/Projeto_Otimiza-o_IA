import numpy as np
import time
import math
from funcao_objetivo import calcular_fo_patio
from logger_config import logger
from excecoes import DadosInconsistentesError
from modelos.solucao import Solucao

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



#Explora o espaco de soluções por um número fixo de iterações
def heuristica_construtiva_iter(
        todos_indices_patios, 
        qtd_patios_selecionar,
        matriz_distancias,
        volumes_arvores,
        distancia_maxima,
        penalizacao_volume,
        rest_vol_sup,
        num_iteracoes
):
    tempo_inicio = time.time()
    cont_viaveis = 0
    
    # Inicializa a melhor solução com distância infinita
    melhor_solucao = Solucao(
        patios_selecionados=[],
        distancia_total=math.inf,
        viavel=False
    )
    
    for _ in range(num_iteracoes):
        res = obter_solucao_aleatoria(
            todos_indices_patios, 
            qtd_patios_selecionar,
            matriz_distancias,
            volumes_arvores,
            distancia_maxima,
            penalizacao_volume,
            rest_vol_sup
        )
        
        # Se encontrou uma distância menor, atualiza a melhor solução
        if res.distancia_total < melhor_solucao.distancia_total:
            melhor_solucao = res
            melhor_solucao.tempo_solucao = time.time() - tempo_inicio
            
        if res.viavel:
            cont_viaveis += 1
            
    melhor_solucao.tempo_total = time.time() - tempo_inicio
    melhor_solucao.num_iteracoes = num_iteracoes
    melhor_solucao.num_viaveis = cont_viaveis
    melhor_solucao.num_inviaveis = num_iteracoes - cont_viaveis
    
    logger.info(f"Heurística Iterativa concluída em {melhor_solucao.tempo_total:.2f}s")
    return melhor_solucao

#Explora o espaço de soluções até atingir um limite de tempo
def heuristica_construtiva_tempo(
        todos_indices_patios, 
        qtd_patios_selecionar,
        matriz_distancias,
        volumes_arvores,
        distancia_maxima,
        penalizacao_volume,
        rest_vol_sup,
        tempo_limite_segundos
):
    tempo_inicio = time.time()
    tempo_fim = tempo_inicio + tempo_limite_segundos
    
    cont_iteracoes = 0
    cont_viaveis = 0
    
    melhor_solucao = Solucao(
        patios_selecionados=[],
        distancia_total=math.inf,
        viavel=False
    )
    
    # Laço roda enquanto o tempo atual for menor que o tempo limite
    while time.time() < tempo_fim:
        cont_iteracoes += 1
        res = obter_solucao_aleatoria(
            todos_indices_patios, 
            qtd_patios_selecionar,
            matriz_distancias,
            volumes_arvores,
            distancia_maxima,
            penalizacao_volume,
            rest_vol_sup
        )
        
        if res.distancia_total < melhor_solucao.distancia_total:
            melhor_solucao = res
            melhor_solucao.tempo_solucao = time.time() - tempo_inicio
            
        if res.viavel:
            cont_viaveis += 1
            
    melhor_solucao.tempo_total = time.time() - tempo_inicio
    melhor_solucao.num_iteracoes = cont_iteracoes
    melhor_solucao.num_viaveis = cont_viaveis
    melhor_solucao.num_inviaveis = cont_iteracoes - cont_viaveis
    
    logger.info(f"Heurística de Tempo concluída ({cont_iteracoes} iterações em {melhor_solucao.tempo_total:.2f}s)")
    return melhor_solucao