class ProjetoOtimizacaoError(Exception):
    #Exceção base para todos os erros do projeto.
    pass


class ArquivoDadosNaoEncontradoError(ProjetoOtimizacaoError):
    #Lançada quando um arquivo de dados (.txt) esperado não existe.
    pass


class ColunaAusenteError(ProjetoOtimizacaoError):
    #Lançada quando o arquivo lido não tem as colunas esperadas.
    pass


class DadosInconsistentesError(ProjetoOtimizacaoError):
    #Lançada quando a matriz de distâncias não bate com árvores/pátios.
    pass