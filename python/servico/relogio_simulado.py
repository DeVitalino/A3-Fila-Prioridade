from datetime import timedelta


class RelogioSimulado:
    # nunca lê o relógio real; o tempo só anda quando o serviço manda
    def __init__(self, data_base):
        self.data_base = data_base
        self.minuto_atual = 0

    def avancar(self, minutos=1):
        if minutos < 1:
            raise ValueError("Só dá para avançar um número positivo de minutos")
        self.minuto_atual += minutos

    def para_datetime(self, minuto):
        return self.data_base + timedelta(minutes=minuto)

    def agora(self):
        return self.para_datetime(self.minuto_atual)
