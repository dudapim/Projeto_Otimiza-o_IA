# ---------------------------------------------------------
# PROJETO DE OTIMIZAÇÃO E INTELIGÊNCIA ARTIFICIAL
# Arquivo principal (Ponto de partida do nosso programa)
# ---------------------------------------------------------

import matplotlib
import numpy as np
import pandas as pd
import scipy

print("🚀 Ambiente virtual configurado e isolado com sucesso!")
print(f"Versão do NumPy: {np.__version__}")
print(f"Versão do Pandas: {pd.__version__}")
print(f"Versão do SciPy: {scipy.__version__}")
print(f"Versão do Matplotlib: {matplotlib.__version__}")

from importador import (
    calcular_matriz_euclidiana,
    criar_mapeamentos_indices,
    importar_arvores,
    importar_matriz_distancias,
    importar_patios,  
)

from excecoes import ProjetoOtimizacaoError
from logger_config import logger
from funcao_objetivo import calcular_fo_patio
from heuristicas import obter_solucao_aleatoria, heuristica_construtiva_iter, heuristica_construtiva_tempo
try:
    # 1º PASSO: IMPORTAÇÃO DOS PÁTIOS 
    patios = importar_patios("data/Patios_Inst_01.txt")

    print("\n--- DADOS DOS PÁTIOS ---")
    print("Quantidade de pátios:", len(patios))

    primeiro_id_patio = list(patios.keys())[0]
    patio_teste = patios[primeiro_id_patio]

    print("Primeiro pátio:")
    print("ID:", patio_teste.id)
    print("Nome:", patio_teste.nome)
    print("X:", patio_teste.x)
    print("Y:", patio_teste.y)

    # 2º PASSO: IMPORTAÇÃO DAS ÁRVORES 
    arvores = importar_arvores("data/Arvores_Inst_01.txt") 

    #Foi adicionado o vetor de volumes para a arvores 
    volumes_arvores = np.array(
        [arvore.volume for arvore in arvores.values()],
        dtype = np.float64
    )
    print("\n--- DADOS DAS ÁRVORES ---")
    print("Quantidade de árvores:", len(arvores))

    primeiro_fid_arvore = list(arvores.keys())[0]
    arvore_teste = arvores[primeiro_fid_arvore]

    print("Primeira árvore:")
    print("FID:", arvore_teste.fid)
    print("Volume:", arvore_teste.volume)
    print("X:", arvore_teste.x)
    print("Y:", arvore_teste.y)

    # 3º PASSO: IMPORTAÇÃO DA MATRIZ DE DISTÂNCIAS REAIS
    matriz_distancias = importar_matriz_distancias(
        "data/Distancias_Inst_01.txt", arvores_dict=arvores, patios_dict=patios
    )

    print("\n--- MATRIZ DE DISTÂNCIAS REAIS ---")
    print("Tipo da matriz:", type(matriz_distancias))
    print(f"Dimensão da matriz (Árvores x Pátios): {matriz_distancias.shape}")
    print("Exemplo [Árvore 0 -> Pátio 0]:", matriz_distancias[0, 0])

    # 4º PASSO: CÁLCULO DAS DISTÂNCIAS EUCLIDIANAS
    matriz_euclidiana = calcular_matriz_euclidiana(arvores, patios)
    print("\n--- MATRIZ DE DISTÂNCIAS EUCLIDIANAS ---")
    print(f"Dimensão da matriz euclidiana: {matriz_euclidiana.shape}")

    # 5º PASSO: CRIAÇÃO DOS MAPEAMENTOS DE ÍNDICES
    fids_ordem, patios_ordem, arvore_para_idx, patio_para_idx = (
        criar_mapeamentos_indices(arvores, patios)
    )

    print("\n--- MAPEAMENTOS CONCLUÍDOS ---")
    print("Total de árvores mapeadas:", len(arvore_para_idx))
    print("Total de pátios mapeados:", len(patio_para_idx))

    # 6º PASSO: VERIFICAÇÃO E COMPARAÇÃO PARA A FUNÇÃO OBJETIVO
    print("\n--- MATRIZES PRONTAS PARA A FUNÇÃO OBJETIVO ---")
    print(f"Shape Matriz Euclidiana: {matriz_euclidiana.shape}")
    print(f"Shape Matriz Distâncias Reais: {matriz_distancias.shape}")

    # Teste de verificação rápida: Árvore FID 1 -> Pátio ID 1
    idx_arv = arvore_para_idx[1]
    idx_pat = patio_para_idx[1]

    print(f"Distância Euclidiana [Árvore 1 -> Pátio 1]: {matriz_euclidiana[idx_arv, idx_pat]:.4f} m")
    print(f"Distância Real       [Árvore 1 -> Pátio 1]: {matriz_distancias[idx_arv, idx_pat]:.4f} m")

    # TESTE DA FO 1 ):
    # Selecionando alguns patios apenas de teste 
    patios_selecionados = [0, 1, 2]

    dist_max = 5000.0
    penalidade = 100.0
    vol_maximo = 10000.0
    
    solucao_atual = calcular_fo_patio(
        matriz_distancias,
        patios_selecionados,
        volumes_arvores,
        dist_max,
        penalidade,
        vol_maximo
    )
    
    print("\n--- TESTE DA FUNÇÃO OBJETIVO ---")
    print("Pátios selecionados:", solucao_atual.patios_selecionados)
    print("Distância total:", solucao_atual.distancia_total)
    print("A solução é viável?", solucao_atual.viavel)

    # 7º PASSO: TESTE DA SOLUÇÃO ALEATÓRIA
    # Criamos a lista de todos os índices possíveis de pátios (0 até n-1)
    todos_indices_patios = list(range(len(patios)))
    
    qtd_patios = 3  # Quantidade de pátios que a heurística deve sortear
    dist_max = 5000.0
    penalidade = 100.0
    vol_maximo = 10000.0
    
    # Chama a nova função que você criou no arquivo heuristicas.py
    solucao_aleatoria = obter_solucao_aleatoria(
        todos_indices_patios,
        qtd_patios,
        matriz_distancias,
        volumes_arvores,
        dist_max,
        penalidade,
        vol_maximo
    )
    
    print("\n--- TESTE DA SOLUÇÃO ALEATÓRIA ---")
    print("Pátios sorteados:", solucao_aleatoria.patios_selecionados)
    print("Distância total (com penalizações):", solucao_aleatoria.distancia_total)
    print("A solução é viável?:", solucao_aleatoria.viavel)

    # 7º PASSO: TESTE DA HEURÍSTICA CONSTRUTIVA
    todos_indices_patios = list(range(len(patios)))
    qtd_patios = 3 
    dist_max = 5000.0
    penalidade = 100.0
    vol_maximo = 10000.0
    
    print("\n--- INICIANDO HEURÍSTICA CONSTRUTIVA (1000 ITERAÇÕES) ---")
    melhor_solucao = heuristica_construtiva_iter(
        todos_indices_patios,
        qtd_patios,
        matriz_distancias,
        volumes_arvores,
        dist_max,
        penalidade,
        vol_maximo,
        num_iteracoes=1000
    )
    
    print("Melhores Pátios:", melhor_solucao.patios_selecionados)
    print(f"Menor Distância Encontrada: {melhor_solucao.distancia_total:.4f}")
    print(f"A solução é viável?: {melhor_solucao.viavel}")
    print(f"Tempo total de busca: {melhor_solucao.tempo_total:.4f}s")
    print(f"Encontrou a melhor solução no tempo: {melhor_solucao.tempo_solucao:.4f}s")
    print(f"Soluções Viáveis: {melhor_solucao.num_viaveis} | Inviáveis: {melhor_solucao.num_inviaveis}")
    
except ProjetoOtimizacaoError as e:
    logger.critical(f"Execução interrompida por erro no domínio da aplicação: {e}")
    print(f"\n❌ Erro: {e}")
    print("Verifique o arquivo de log em logs/ para mais detalhes.")

except Exception as e:
    # Captura qualquer erro inesperado que não seja das nossas exceções customizadas
    logger.exception(f"Erro inesperado durante a execução: {e}")
    print(f"\n❌ Erro inesperado: {e}")
    print("Verifique o arquivo de log em logs/ para mais detalhes.")




