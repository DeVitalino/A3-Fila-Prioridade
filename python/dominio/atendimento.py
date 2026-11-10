class Atendimento:
    def __init__(self, cliente, id_guiche, minuto_inicio, sla_minutos, motivo):
        self.id_atendimento = 0  # o repositório preenche
        self.cliente = cliente
        self.id_guiche = id_guiche
        self.minuto_inicio = minuto_inicio
        self.minuto_fim = minuto_inicio + cliente.tipo_servico.minutos
        self.tempo_espera = minuto_inicio - cliente.minuto_chegada
        self.sla_minutos = sla_minutos
        self.motivo = motivo  # NORMAL, AGING ou COTA

    @property
    def dentro_sla(self):
        return self.tempo_espera <= self.sla_minutos

    @property
    def status_sla(self):
        return "DENTRO" if self.dentro_sla else "FORA"
