from dataclasses import dataclass
from typing import List

@dataclass
class Solucao:
    patios_selecionados: List[int]
    distancia_total: float
    viavel: bool