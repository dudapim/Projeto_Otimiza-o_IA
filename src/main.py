# ---------------------------------------------------------
# PROJETO DE OTIMIZAÇÃO E INTELIGÊNCIA ARTIFICIAL
# Arquivo principal (Ponto de partida do nosso programa)
# ---------------------------------------------------------

# Importação das bibliotecas essenciais para Ciência de Dados e IA:
import numpy as np       # Usada para cálculos matemáticos rápidos, vetores e matrizes pesadas
import pandas as pd      # Usada para manipulação e análise de tabelas de dados (lê arquivos CSV, Excel, etc.)
import scipy             # Usada para funções matemáticas complexas e algoritmos de otimização
import matplotlib        # Usada para criar gráficos e visualizações dos resultados

# Mensagem de sucesso para confirmar que o ambiente está rodando corretamente
print("🚀 Ambiente virtual configurado e isolado com sucesso!")

# Impressão das versões instaladas (Isso serve para garantir que o Docker e a .venv carregaram as bibliotecas certas)
print(f"Versão do NumPy: {np.__version__}")
print(f"Versão do Pandas: {pd.__version__}")
print(f"Versão do SciPy: {scipy.__version__}")
print(f"Versão do Matplotlib: {matplotlib.__version__}")

# Importação das funções responsáveis por importar os dados
from importador import importar_patios, importar_arvores

# 1º PASSO: IMPORTAÇÃO DOS PÁTIOS (Exigência: Pátios antes das árvores)
# ---------------------------------------------------------
patios = importar_patios("data/Patios_Inst_01.txt")

print("\n--- DADOS DOS PÁTIOS ---")
print("Quantidade de pátios:", len(patios))
print("Primeiro pátio:")
print("ID:", patios[0].id)
print("Nome:", patios[0].nome)
print("X:", patios[0].x)
print("Y:", patios[0].y)


# 2º PASSO: IMPORTAÇÃO DAS ÁRVORES 
# ---------------------------------------------------------
arvores = importar_arvores("data/Arvores_Inst_01.txt") 

print("\n--- DADOS DAS ÁRVORES ---")
print("Quantidade de árvores:", len(arvores))
print("Primeira árvore:")
print("ID:", arvores[0].id)
print("Volume:", arvores[0].volume)
print("X:", arvores[0].x)
print("Y:", arvores[0].y)