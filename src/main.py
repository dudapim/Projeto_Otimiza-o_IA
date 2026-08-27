# ---------------------------------------------------------
# PROJETO DE OTIMIZAÇÃO E INTELIGÊNCIA ARTIFICIAL
# Arquivo principal (Ponto de partida do nosso programa)
# ---------------------------------------------------------

import numpy as np
import pandas as pd
import scipy
import matplotlib

print("🚀 Ambiente virtual configurado e isolado com sucesso!")
print(f"Versão do NumPy: {np.__version__}")
print(f"Versão do Pandas: {pd.__version__}")
print(f"Versão do SciPy: {scipy.__version__}")
print(f"Versão do Matplotlib: {matplotlib.__version__}")

from importador import importar_patios, importar_arvores

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