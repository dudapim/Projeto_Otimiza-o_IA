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

# 1º PASSO: IMPORTAÇÃO DOS PÁTIOS 
# ---------------------------------------------------------
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
# ---------------------------------------------------------
arvores = importar_arvores("data/Arvores_Inst_01.txt") 

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
# ---------------------------------------------------------
matriz_distancias = importar_matriz_distancias(
    "data/Distancias_Inst_01.txt", arvores_dict=arvores, patios_dict=patios
)

print("\n--- MATRIZ DE DISTÂNCIAS REAIS ---")
print("Tipo da matriz:", type(matriz_distancias))
print(f"Dimensão da matriz (Árvores x Pátios): {matriz_distancias.shape}")
print("Exemplo [Árvore 0 -> Pátio 0]:", matriz_distancias[0, 0])

# 4º PASSO: CÁLCULO DAS DISTÂNCIAS EUCLIDIANAS
# ---------------------------------------------------------
matriz_euclidiana = calcular_matriz_euclidiana(arvores, patios)
print("\n--- MATRIZ DE DISTÂNCIAS EUCLIDIANAS ---")
print(f"Dimensão da matriz euclidiana: {matriz_euclidiana.shape}")

# 5º PASSO: CRIAÇÃO DOS MAPEAMENTOS DE ÍNDICE
# ---------------------------------------------------------
fids_ordem, patios_ordem, arvore_para_idx, patio_para_idx = (
    criar_mapeamentos_indices(arvores, patios)
)

print("\n--- MAPEAMENTOS CONCLUÍDOS ---")
print("Total de árvores mapeadas:", len(arvore_para_idx))
print("Total de pátios mapeados:", len(patio_para_idx))

# 6º PASSO: VERIFICAÇÃO E COMPARAÇÃO PARA A FUNÇÃO OBJETIVO
# ---------------------------------------------------------
print("\n--- MATRIZES PRONTAS PARA A FUNÇÃO OBJETIVO ---")
print(f"Shape Matriz Euclidiana: {matriz_euclidiana.shape}")
print(f"Shape Matriz Distâncias Reais: {matriz_distancias.shape}")

# Teste de verificação rápida: Árvore FID 1 -> Pátio ID 1
idx_arv = arvore_para_idx[1]
idx_pat = patio_para_idx[1]

print(f"Distância Euclidiana [Árvore 1 -> Pátio 1]: {matriz_euclidiana[idx_arv, idx_pat]:.4f} m")
print(f"Distância Real       [Árvore 1 -> Pátio 1]: {matriz_distancias[idx_arv, idx_pat]:.4f} m")