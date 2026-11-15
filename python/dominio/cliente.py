class Cliente:
    def __init__(self, id_cliente, senha, categoria, tipo_servico, minuto_chegada, idade):
        self.id_cliente = id_cliente
        self.senha = senha
        self.categoria = categoria
        self.tipo_servico = tipo_servico
        self.minuto_chegada = minuto_chegada
        self.idade = idade
        self.pontuacao_inicial = categoria.pontuacao_inicial
        self.pontuacao_atual = categoria.pontuacao_inicial
        self.alerta_sla_emitido = False
        self.starvation_detectado = False

    def espera(self, minuto_atual):
        """Retorna o tempo de espera em minutos."""
        return minuto_atual - self.minuto_chegada

    def calcular_pontuacao(self, minuto_atual):
        """
        Calcula a pontuação atual baseada no aging.
        
        Fórmula: pontuacao_atual = pontuacao_inicial × 1,6^n
        Onde n = quantidade de períodos completos de 20 minutos
        
        EXCEÇÃO: NIVEL_4 (80+ anos) mantém prioridade absoluta.
        """
        from dominio.categoria import Categoria
        
        # Nível 4 sempre tem prioridade absoluta
        if self.categoria == Categoria.NIVEL_4:
            return float('-inf')
        
        # Calcular períodos completos de 20 minutos
        espera = self.espera(minuto_atual)
        periodos = espera // 20
        
        # Aplicar multiplicador 1.6 por período
        self.pontuacao_atual = self.pontuacao_inicial * (1.6 ** periodos)
        return self.pontuacao_atual

    @property
    def prioridade_efetiva(self):
        """
        Compatibilidade com código legado.
        Retorna a pontuação atual (quanto menor, maior prioridade).
        """
        from dominio.categoria import Categoria
        
        if self.categoria == Categoria.NIVEL_4:
            return float('-inf')
        return -self.pontuacao_atual  # Negativo para ordenação correta

    @prioridade_efetiva.setter
    def prioridade_efetiva(self, valor):
        """Setter para compatibilidade com código legado."""
        if self.categoria.value != -1:  # Não atualiza NIVEL_4
            self.pontuacao_atual = -valor

    def chave(self):
        """
        Chave de ordenação para o heap (min-heap).
        Tupla: (prioridade_invertida, id_cliente)
        
        Para min-heap funcionar corretamente:
        - Menor valor = maior prioridade
        - NIVEL_4 precisa ter o MENOR valor possível
        - Empate resolvido por ordem de chegada (id_cliente)
        """
        from dominio.categoria import Categoria
        
        if self.categoria == Categoria.NIVEL_4:
            # Menor valor possível = sempre primeiro
            return (float('-inf'), self.id_cliente)
        
        # Negativo da pontuação: quanto MAIOR a pontuação, MENOR o valor (maior prioridade)
        return (-self.pontuacao_atual, self.id_cliente)

    def __repr__(self):
        return f"Cliente({self.senha}, {self.categoria.nome_curto}, {self.idade}a, pont={self.pontuacao_atual:.2f})"
