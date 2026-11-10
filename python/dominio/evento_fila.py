from enum import Enum


class TipoEvento(Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
    ALERTA_SLA = "ALERTA_SLA"
    STARVATION = "STARVATION"


class EventoFila:
    def __init__(self, tipo, minuto, cliente, id_guiche=None, tempo_espera=0,
                 status_sla=None, observacao=None):
        self.id_evento = 0  # o repositório preenche
        self.tipo = tipo
        self.minuto = minuto
        self.cliente = cliente
        self.id_guiche = id_guiche
        self.tempo_espera = tempo_espera
        self.status_sla = status_sla
        self.observacao = observacao
