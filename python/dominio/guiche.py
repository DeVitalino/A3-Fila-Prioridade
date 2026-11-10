class Guiche:
    def __init__(self, numero):
        self.numero = numero
        self.cliente_atual = None
        self.minuto_fim = 0
        self.total_atendidos = 0

    def esta_livre(self):
        return self.cliente_atual is None

    def iniciar(self, cliente, minuto_inicio):
        if not self.esta_livre():
            raise ValueError(f"Guichê {self.numero} já está ocupado")
        self.cliente_atual = cliente
        self.minuto_fim = minuto_inicio + cliente.tipo_servico.minutos

    def liberar(self):
        self.cliente_atual = None
        self.total_atendidos += 1
