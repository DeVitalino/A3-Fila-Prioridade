from enum import Enum


class Categoria(Enum):
    # menor valor = mais prioridade
    PRIORITARIO = 0
    VIP = 1
    COMUM = 2

    @property
    def prioridade_base(self):
        return self.value

    @property
    def descricao(self):
        if self == Categoria.PRIORITARIO:
            return "Prioritário (idoso 60+, gestante, PCD, lactante)"
        if self == Categoria.VIP:
            return "Preferencial / VIP"
        return "Comum"

    @property
    def prefixo_senha(self):
        return {"PRIORITARIO": "P", "VIP": "V", "COMUM": "C"}[self.name]
