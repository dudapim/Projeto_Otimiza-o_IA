# Teste inicial (placeholder) apenas para validar se a estrutura de testes está funcionando.
# No futuro, será substituído pelos testes reais das fórmulas de otimização e IA.
import numpy as np
from importador import (
    importar_patios,
    importar_arvores,
    importar_matriz_distancias,
    calcular_matriz_euclidiana,
)


def test_matriz_distancias():
    patios = importar_patios("data/Patios_Inst_01.txt")
    arvores = importar_arvores("data/Arvores_Inst_01.txt")

    matriz_dist = importar_matriz_distancias(
        "data/Distancias_Inst_01.txt", arvores, patios
    )
    matriz_eucl = calcular_matriz_euclidiana(arvores, patios)

    # 1. Deve ser do tipo ndarray
    assert isinstance(matriz_dist, np.ndarray)

    # 2. As dimensões de ambas devem ser estritamente iguais: (len(arvores), len(patios))
    assert matriz_dist.shape == matriz_eucl.shape
    assert matriz_dist.shape == (len(arvores), len(patios))

    # 3. Não pode conter valores nulos (NaN)
    assert not np.isnan(matriz_dist).any()