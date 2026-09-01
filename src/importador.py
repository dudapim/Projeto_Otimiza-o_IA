# Importação da biblioteca Pandas
import pandas as pd

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


#Função responsável por ler o arquivo de árvores e retornar um dicionário de objetos.
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