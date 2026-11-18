from dataclasses import dataclass, field
from datetime import datetime

from dominio.categoria import Categoria


def sla_padrao():
    """
    SLAs ajustados para os 4 níveis:
    - NIVEL_4 (80+): 10 minutos
    - NIVEL_3 (60-79): 15 minutos  
    - NIVEL_2 (PCD): 20 minutos
    - NIVEL_1 (Comum): 30 minutos
    """
    return {
        Categoria.NIVEL_4: 10,
        Categoria.NIVEL_3: 15,
        Categoria.NIVEL_2: 20,
        Categoria.NIVEL_1: 30
    }


@dataclass
class Configuracao:
    qtd_guiches: int = 3
    data_base: datetime = datetime(2026, 11, 9, 8, 0, 0)

    # Aging: FIXO em 20 minutos e multiplicador 1.6
    aging_ativo: bool = True
    intervalo_recalculo: int = 5  # Recalcular a cada 5 minutos

    # Cota: depois de "cota_n" prioritários seguidos, chama um comum
    cota_ativa: bool = True
    cota_n: int = 3

    sla: dict = field(default_factory=sla_padrao)
    percentual_alerta_sla: float = 0.8
    limite_starvation: int = 40

    # Parâmetros legados para compatibilidade com testes
    @property
    def minutos_por_nivel(self):
        """Compatibilidade: sempre retorna 20 (aging fixo)."""
        return 20

    def validar(self):
        if self.qtd_guiches < 1:
            raise ValueError("Precisa de pelo menos 1 guichê")
        if self.intervalo_recalculo < 1:
            raise ValueError("Intervalo de recálculo deve ser maior que zero")
        if self.cota_n < 1:
            raise ValueError("A cota deve ser maior que zero")
        if not 0 < self.percentual_alerta_sla <= 1:
            raise ValueError("O percentual de alerta deve estar entre 0 e 1")
        if self.limite_starvation < 1:
            raise ValueError("O limite de starvation deve ser maior que zero")
        if set(self.sla) != set(Categoria):
            raise ValueError("É necessário definir o tempo máximo de espera para os quatro níveis")
        if any(not isinstance(minutos, int) or minutos < 1 for minutos in self.sla.values()):
            raise ValueError("O tempo máximo de espera de cada nível deve ser um número inteiro maior que zero")
