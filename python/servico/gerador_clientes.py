import random

from dominio.categoria import Categoria


class GeradorClientes:
    def __init__(self, tipos_servico, semente=None, chance_chegada=0.15):
        self.tipos_servico = tipos_servico
        self.chance_chegada = chance_chegada
        self.aleatorio = random.Random(semente)

    def sortear_categoria_e_idade(self):
        """
        Sorteia categoria e idade compatível.
        
        Distribuição:
        - 1% → NIVEL_4 (80+ anos) - RARO!
        - 12% → NIVEL_3 (60-79 anos)
        - 10% → NIVEL_2 (PCD, qualquer idade)
        - 77% → NIVEL_1 (Comum, qualquer idade)
        """
        valor = self.aleatorio.random()
        
        # 1% - Nível 4: 80+ anos (prioridade absoluta)
        if valor < 0.01:
            idade = self.aleatorio.randint(80, 95)
            return Categoria.NIVEL_4, idade
        
        # 12% - Nível 3: 60-79 anos
        if valor < 0.13:  # 0.01 + 0.12 = 0.13
            idade = self.aleatorio.randint(60, 79)
            return Categoria.NIVEL_3, idade
        
        # 10% - Nível 2: PCD (qualquer idade adulta)
        if valor < 0.23:  # 0.13 + 0.10 = 0.23
            idade = self.aleatorio.randint(18, 70)
            return Categoria.NIVEL_2, idade
        
        # 77% - Nível 1: Sem prioridade
        idade = self.aleatorio.randint(18, 59)
        return Categoria.NIVEL_1, idade

    def sortear_cliente(self):
        """Sorteia uma categoria, idade e tipo de serviço."""
        categoria, idade = self.sortear_categoria_e_idade()
        tipo = self.aleatorio.choice(self.tipos_servico)
        return categoria, idade, tipo

    def chegadas_no_minuto(self):
        """
        Simula chegadas aleatórias em um minuto.
        Retorna lista de tuplas (categoria, idade, tipo_servico).
        """
        novos = []
        for _ in range(2):  # Até 2 chegadas por minuto
            if self.aleatorio.random() < self.chance_chegada:
                novos.append(self.sortear_cliente())
        return novos
