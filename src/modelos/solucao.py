from dataclasses import dataclass
from typing import List

@dataclass
class Solucao:
    patios_selecionados: List[int]
    distancia_total: float
    viavel: bool
    tempo_solucao: float = 0.0
    tempo_total: float = 0.0
    num_iteracoes: int = 0
    num_viaveis: int = 0
    num_inviaveis: int = 0


