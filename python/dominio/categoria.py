from enum import Enum


class Categoria(Enum):
    """
    Sistema de 4 níveis de prioridade baseado em idade e deficiência.
    
    Menor valor numérico = MAIOR prioridade no heap (min-heap).
    """
    # Valor negativo para garantir prioridade ABSOLUTA no heap
    NIVEL_4 = -1  # 80+ anos (PRIORIDADE ABSOLUTA)
    NIVEL_3 = 3   # 60-79 anos
    NIVEL_2 = 2   # Pessoas com deficiência (qualquer idade)
    NIVEL_1 = 1   # Sem prioridade especial

    @property
    def pontuacao_inicial(self):
        """
        Pontuação base para o algoritmo de aging.
        NIVEL_4 não usa aging (prioridade absoluta).
        """
        if self == Categoria.NIVEL_4:
            return float('-inf')  # Sempre primeiro
        return abs(self.value)

    @property
    def descricao(self):
        descricoes = {
            Categoria.NIVEL_4: "Nível 4: 80 anos ou mais (prioridade absoluta)",
            Categoria.NIVEL_3: "Nível 3: 60 a 79 anos",
            Categoria.NIVEL_2: "Nível 2: Pessoas com deficiência",
            Categoria.NIVEL_1: "Nível 1: Sem prioridade especial"
        }
        return descricoes[self]

    @property
    def prefixo_senha(self):
        prefixos = {
            Categoria.NIVEL_4: "N4",
            Categoria.NIVEL_3: "N3",
            Categoria.NIVEL_2: "N2",
            Categoria.NIVEL_1: "N1"
        }
        return prefixos[self]

    @property
    def nome_curto(self):
        """Nome para exibição em tabelas."""
        nomes = {
            Categoria.NIVEL_4: "80+ anos",
            Categoria.NIVEL_3: "60-79 anos",
            Categoria.NIVEL_2: "PCD",
            Categoria.NIVEL_1: "Comum"
        }
        return nomes[self]

    @staticmethod
    def por_idade(idade, tem_deficiencia=False):
        """
        Determina a categoria baseado na idade e presença de deficiência.
        
        Regras:
        - 80+ anos sempre é NIVEL_4 (independente de deficiência)
        - 60-79 anos é NIVEL_3 (independente de deficiência)  
        - Qualquer idade com deficiência é NIVEL_2
        - Sem prioridade é NIVEL_1
        """
        if idade >= 80:
            return Categoria.NIVEL_4
        if idade >= 60:
            return Categoria.NIVEL_3
        if tem_deficiencia:
            return Categoria.NIVEL_2
        return Categoria.NIVEL_1
