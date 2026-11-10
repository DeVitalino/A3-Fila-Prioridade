import random

from dominio.categoria import Categoria


class GeradorClientes:
    def __init__(self, tipos_servico, semente=None, chance_chegada=0.15):
        self.tipos_servico = tipos_servico
        self.chance_chegada = chance_chegada
        self.aleatorio = random.Random(semente)

    def sortear_categoria(self):
        # 20% prioritário, 20% vip, 60% comum
        valor = self.aleatorio.random()
        if valor < 0.20:
            return Categoria.PRIORITARIO
        if valor < 0.40:
            return Categoria.VIP
        return Categoria.COMUM

    def sortear_cliente(self):
        categoria = self.sortear_categoria()
        tipo = self.aleatorio.choice(self.tipos_servico)
        return categoria, tipo

    def chegadas_no_minuto(self):
        # até 2 chegadas por minuto
        novos = []
        for _ in range(2):
            if self.aleatorio.random() < self.chance_chegada:
                novos.append(self.sortear_cliente())
        return novos
