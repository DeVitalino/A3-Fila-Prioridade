class Cliente:
    def __init__(self, id_cliente, senha, categoria, tipo_servico, minuto_chegada):
        self.id_cliente = id_cliente
        self.senha = senha
        self.categoria = categoria
        self.tipo_servico = tipo_servico
        self.minuto_chegada = minuto_chegada
        self.prioridade_efetiva = categoria.prioridade_base
        self.alerta_sla_emitido = False
        self.starvation_detectado = False

    def espera(self, minuto_atual):
        return minuto_atual - self.minuto_chegada

    def chave(self):
        # desempate por id_cliente, que cresce na ordem de chegada (FIFO)
        return (self.prioridade_efetiva, self.id_cliente)

    def __repr__(self):
        return f"Cliente({self.senha}, prio={self.prioridade_efetiva})"
