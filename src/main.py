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