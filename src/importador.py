# Importação das bibliotecas necessárias
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

# Importação das classes modelo que estruturam os nossos dados
from modelos.patio import Patio
from modelos.arvore import Arvore

# Função responsável por ler o arquivo de pátios e retornar um dicionário de objetos.
def importar_patios(caminho_arquivo):

    # Criamos um dicionário vazio 
    patios_dict = {} 
    
    # O Pandas lê o arquivo TXT inteiro de uma só vez.
    df_patios = pd.read_csv(caminho_arquivo, sep='\t')
    
    # Percorrendo as linhas.
    for linha in df_patios.itertuples():
        
        # Instanciamos um novo objeto Patio, o Pandas permite acessar as colunas como se fossem atributos.     
        patio = Patio(linha.id, linha.nome, linha.x, linha.y)
        
        # Guardamos o objeto instanciado dentro do dicionário.
        patios_dict[linha.id] = patio 
        
    return patios_dict


# Função responsável por ler o arquivo de árvores e retornar um dicionário de objetos.
def importar_arvores(caminho_arquivo):
    
    # Dicionário para garantir a busca instantânea.
    arvores_dict = {} 
    
    # Leitura do arquivo TXT com Pandas
    df_arvores = pd.read_csv(caminho_arquivo, sep='\t')
    
    # Iteração pelas linhas da tabela de árvores.
    for linha in df_arvores.itertuples():
        
        # Instanciamos o objeto Arvore buscando exatamente os nomes das colunas
        arvore = Arvore(linha.FID, linha.POINT_X, linha.POINT_Y, linha.Volume_Eq)
        
        # Armazenamos a árvore no dicionário usando o FID como chave.
        arvores_dict[linha.FID] = arvore 
        
    return arvores_dict


# Função responsável por ler o arquivo de distâncias e retornar uma matriz NumPy.
def importar_matriz_distancias(caminho_arquivo, arvores_dict, patios_dict):

    # O Pandas lê o arquivo TXT inteiro de uma só vez.
    df_dist = pd.read_csv(caminho_arquivo, sep="\t")

    # Pivotamos os dados para cruzar árvores nas linhas e pátios nas colunas.
    df_pivot = df_dist.pivot(
        index="arvore", columns="patio", values="distancia_total"
    )

    # Buscamos as chaves ordenadas para garantir a correspondência correta.
    fids_arvores = list(arvores_dict.keys())
    ids_patios = list(patios_dict.keys())

    # Reindexamos a tabela para alinhar exatamente com as árvores e pátios.
    df_pivot = df_pivot.reindex(index=fids_arvores, columns=ids_patios)

    # Convertemos a tabela em uma matriz numérica pura do NumPy.
    matriz_distancias = df_pivot.to_numpy(dtype=np.float64)

    return matriz_distancias


# Função responsável por calcular a matriz euclidiana (N x M) e retorná-la para uso na FO.
def calcular_matriz_euclidiana(arvores_dict, patios_dict):

    # Extraímos as coordenadas (X, Y) de todas as árvores em um array NumPy bidimensional.
    coords_arvores = np.array(
        [[arv.x, arv.y] for arv in arvores_dict.values()], dtype=np.float64
    )

    # Extraímos as coordenadas (X, Y) de todos os pátios em um array NumPy bidimensional.
    coords_patios = np.array(
        [[pat.x, pat.y] for pat in patios_dict.values()], dtype=np.float64
    )

    # O cdist calcula a distância euclidiana entre cada par de árvore e pátio em C puro.
    matriz_euclidiana = cdist(coords_arvores, coords_patios, metric="euclidean")

    return matriz_euclidiana


# Conversor bidirecional entre os IDs reais dos arquivos e as posições (índices de 0 a n-1) das linhas e colunas da matriz NumPy
# Função responsável por criar as tabelas de mapeamento entre IDs reais e índices da matriz.
def criar_mapeamentos_indices(arvores_dict, patios_dict):

    # Listas ordenadas que mapeiam: índice da matriz -> ID real
    fids_arvores = list(arvores_dict.keys()) 
    ids_patios = list(patios_dict.keys())

    # Dicionários reversos que mapeiam: ID real -> índice da matriz
    # enumerate() percorre a lista de IDs atribuindo um contador automático que começa em 0
    arvore_para_idx = {fid: idx for idx, fid in enumerate(fids_arvores)}
    patio_para_idx = {pid: idx for idx, pid in enumerate(ids_patios)}

    return fids_arvores, ids_patios, arvore_para_idx, patio_para_idx