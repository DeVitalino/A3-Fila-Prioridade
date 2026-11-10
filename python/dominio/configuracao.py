from dataclasses import dataclass, field
from datetime import datetime

from dominio.categoria import Categoria


def sla_padrao():
    return {Categoria.PRIORITARIO: 15, Categoria.VIP: 10, Categoria.COMUM: 30}


@dataclass
class Configuracao:
    qtd_guiches: int = 3
    data_base: datetime = datetime(2026, 11, 9, 8, 0, 0)

    # aging: a cada "minutos_por_nivel" esperando, o cliente sobe 1 nível
    aging_ativo: bool = True
    minutos_por_nivel: int = 10
    intervalo_recalculo: int = 5

    # cota: depois de "cota_n" prioritários seguidos, chama um comum
    cota_ativa: bool = True
    cota_n: int = 3

    sla: dict = field(default_factory=sla_padrao)
    percentual_alerta_sla: float = 0.8
    limite_starvation: int = 40

    def validar(self):
        if self.qtd_guiches < 1:
            raise ValueError("Precisa de pelo menos 1 guichê")
        if self.minutos_por_nivel < 1 or self.intervalo_recalculo < 1:
            raise ValueError("Parâmetros de aging devem ser maiores que zero")
        if self.cota_n < 1:
            raise ValueError("A cota deve ser maior que zero")
        if not 0 < self.percentual_alerta_sla <= 1:
            raise ValueError("O percentual de alerta deve estar entre 0 e 1")
        if self.limite_starvation < 1:
            raise ValueError("O limite de starvation deve ser maior que zero")
