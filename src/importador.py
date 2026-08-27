# Importando as classes #
from modelos.patio import Patio
from modelos.arvore import Arvore

def importar_patios(caminho_arquivo):
    patios = [] # Lista de patios #

    with open(caminho_arquivo, "r") as arquivo:
        next(arquivo) # Ignora o cabeçalho #

        for linha in arquivo: # Percorrer o arquivo #
            dados = linha.strip().split("\t") # Tabulação #

            id = int(dados[0])
            nome = dados[1]
            x = float(dados[2]) 
            y = float(dados[3])

            patio = Patio(id, nome, x, y)
            patios.append(patio) # Adiciona o objeto a lista #

    return patios

def importar_arvores(caminho_arquivo):
    arvores = [] # Lista de árvores #

    with open(caminho_arquivo, "r") as arquivo:
        next(arquivo) # Ignora o cabeçalho #

        for linha in arquivo: # Percorrer o arquivo #
            dados = linha.strip().split("\t") # Tabulação #

            # Pegando as informações baseadas nas posições exatas do seu TXT
            id = int(dados[0])          # Coluna FID (Índice 0)
            volume = float(dados[4])    # Coluna Volume_Eq (Índice 4)
            x = float(dados[6])         # Coluna POINT_X (Índice 6)
            y = float(dados[7])         # Coluna POINT_Y (Índice 7)

            arvore = Arvore(id, x, y, volume)
            arvores.append(arvore) # Adiciona o objeto a lista #

    return arvores