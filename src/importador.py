# Importação das bibliotecas necessárias
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

# Importação das classes modelo que estruturam os nossos dados
from modelos.patio import Patio
from modelos.arvore import Arvore
from excecoes import ArquivoDadosNaoEncontradoError, ColunaAusenteError, DadosInconsistentesError
from logger_config import logger

# Função responsável por ler o arquivo de pátios e retornar um dicionário de objetos.
def importar_patios(caminho_arquivo):

    # Criamos um dicionário vazio 
    patios_dict = {} 
    
    # O Pandas lê o arquivo TXT inteiro de uma só vez.
    try:
        df_patios = pd.read_csv(caminho_arquivo, sep='\t')
    except FileNotFoundError:
        logger.error(f"Arquivo de pátios não encontrado: {caminho_arquivo}")
        raise ArquivoDadosNaoEncontradoError (f"Arquivo de pátios não encontrado: {caminho_arquivo}")
    except pd.errors.EmptyDataError:
        logger.error(f"Arquivo de pátios está vazio: {caminho_arquivo}")
        raise DadosInconsistentesError(f"Arquivo de pátios vazio: {caminho_arquivo}")

    # Percorrendo as linhas.
    try:
        for linha in df_patios.itertuples():
            # Instanciamos um novo objeto Patio, o Pandas permite acessar as colunas como se fossem atributos.     
            patio = Patio(linha.id, linha.nome, linha.x, linha.y)
        
            # Guardamos o objeto instanciado dentro do dicionário.
            patios_dict[linha.id] = patio 
    except AttributeError as e:
        logger.error(f"Coluna esperada ausente no arquivo de pátios: {e}")
        raise ColunaAusenteError(f"O arquivo de pátios não contém as colunas esperadas(id, nome, x, y): {e}")

    logger.info(f"{len(patios_dict)} pátios importados com sucesso de {caminho_arquivo}")
    return patios_dict


# Função responsável por ler o arquivo de árvores e retornar um dicionário de objetos.
def importar_arvores(caminho_arquivo):
    
    # Dicionário para garantir a busca instantânea.
    arvores_dict = {} 
    
    # Leitura do arquivo TXT com Pandas
    try: 
        df_arvores = pd.read_csv(caminho_arquivo, sep='\t')
    except FileNotFoundError:
        logger.error(f"Arquivo de árvores não encontrado: {caminho_arquivo}")
        raise ArquivoDadosNaoEncontradoError(f"Arquivo de árvore não encontrado: {caminho_arquivo}")
    except pd.errors.EmptyDataError:
        logger.error(f"Arquivo de árvores está vazio: {caminho_arquivo}")
        raise DadosInconsistentesError(f"Arquivo de árvores vazio: {caminho_arquivo}")

    
    # Iteração pelas linhas da tabela de árvores.
    try:
        for linha in df_arvores.itertuples():
            # Instanciamos o objeto Arvore buscando exatamente os nomes das colunas
            arvore = Arvore(linha.FID, linha.POINT_X, linha.POINT_Y, linha.Volume_Eq)

            # Armazenamos a árvore no dicionário usando o FID como chave.
            arvores_dict[linha.FID] = arvore 
    except AttributeError as e:
        logger.error(f"Coluna esperada ausente no arquivo de árvores: {e}")
        raise ColunaAusenteError(f"O arquivo de árvores não contém as colunas esperadas (FID, POINT_X, POINT_Y, Volume_Eq): {e}")

    logger.info(f"{len(arvores_dict)} árvores importadas com sucesso de {caminho_arquivo}")
    return arvores_dict


# Função responsável por ler o arquivo de distâncias e retornar uma matriz NumPy.
def importar_matriz_distancias(caminho_arquivo, arvores_dict, patios_dict):
    try:
        # O Pandas lê o arquivo TXT inteiro de uma só vez.
        df_dist = pd.read_csv(caminho_arquivo, sep="\t")
    except FileNotFoundError:
        logger.error(f"Arquivo de distâncias não encontrado: {caminho_arquivo}")
        raise ArquivoDadosNaoEncontradoError(f"Arquivo de distâncias não encontrados: {caminho_arquivo}")

    try:
        # Pivotamos os dados para cruzar árvores nas linhas e pátios nas colunas.
        df_pivot = df_dist.pivot(index="arvore", columns="patio", values="distancia_total")
    except KeyError as e:
        logger.error(f"Coluna esperada ausente no arquivo de distâncias: {e}")
        raise ColunaAusenteError(f"O arquivo de distâncias precisa das colunas 'arvore', 'patio' e 'distancia_total': {e}")

    # Buscamos as chaves ordenadas para garantir a correspondência correta.
    fids_arvores = list(arvores_dict.keys())
    ids_patios = list(patios_dict.keys())

    # Reindexamos a tabela para alinhar exatamente com as árvores e pátios.
    df_pivot = df_pivot.reindex(index=fids_arvores, columns=ids_patios)

    # Convertemos a tabela em uma matriz numérica pura do NumPy.
    matriz_distancias = df_pivot.to_numpy(dtype=np.float64)

    if np.isnan(matriz_distancias).any():
        qtd_nan = np.isnan(matriz_distancias).sum()
        logger.warning(
            f"Matriz de distâncias contém {qtd_nan} valor ausentes (NaN)"
            f"após reindexação - verifique se todas as combinações árvore-pátio existem no arquivo"
        )
    logger.info(f"Matriz de distâncias importada com sucesso: shape {matriz_distancias.shape}")

    return matriz_distancias


# Função responsável por calcular a matriz euclidiana (N x M) e retorná-la para uso na FO.
def calcular_matriz_euclidiana(arvores_dict, patios_dict):

    try:
        # Extraímos as coordenadas (X, Y) de todas as árvores em um array NumPy bidimensional.
        coords_arvores = np.array(
            [[arv.x, arv.y] for arv in arvores_dict.values()], dtype=np.float64
        )

        # Extraímos as coordenadas (X, Y) de todos os pátios em um array NumPy bidimensional.
        coords_patios = np.array(
            [[pat.x, pat.y] for pat in patios_dict.values()], dtype=np.float64
        )
    except AttributeError as e:
        logger.error(f"Objeto Arvore ou Patio sem atributos x/y válidos: {e}")
        raise DadosInconsistentesError(
            f"Erro ao extrair coordenadas de árvores/pátios: {e}"
        )

    if coords_arvores.size == 0 or coords_patios.size == 0:
        logger.error("Dicionário de árvores ou pátios está vazio — impossível calcular distâncias.")
        raise DadosInconsistentesError(
            "Não é possível calcular a matriz euclidiana com árvores ou pátios vazios."
        )
    
    # O cdist calcula a distância euclidiana entre cada par de árvore e pátio em C puro.
    matriz_euclidiana = cdist(coords_arvores, coords_patios, metric="euclidean")

    logger.info(
        f"Matriz euclidiana calculada com sucesso: shape {matriz_euclidiana.shape}"
    )
    return matriz_euclidiana


# Conversor bidirecional entre os IDs reais dos arquivos e as posições (índices de 0 a n-1) das linhas e colunas da matriz NumPy
# Função responsável por criar as tabelas de mapeamento entre IDs reais e índices da matriz.
def criar_mapeamentos_indices(arvores_dict, patios_dict):
    if not arvores_dict or not patios_dict:
        logger.error("Tentativa de criar mapeamento com dicionário de árvores ou pátios vazio.")
        raise DadosInconsistentesError(
            "Dicionário de árvores ou pátios está vazio — não é possível mapear índices."
        )
    # Listas ordenadas que mapeiam: índice da matriz -> ID real
    fids_arvores = list(arvores_dict.keys()) 
    ids_patios = list(patios_dict.keys())

    # Dicionários reversos que mapeiam: ID real -> índice da matriz
    # enumerate() percorre a lista de IDs atribuindo um contador automático que começa em 0
    arvore_para_idx = {fid: idx for idx, fid in enumerate(fids_arvores)}
    patio_para_idx = {pid: idx for idx, pid in enumerate(ids_patios)}

    logger.info("Mapeamentos de índices criados com sucesso.")
    return fids_arvores, ids_patios, arvore_para_idx, patio_para_idx