class TipoServico:
    def __init__(self, nome, minutos):
        if minutos <= 0:
            raise ValueError("O tempo do serviço deve ser maior que zero")
        self.nome = nome
        self.minutos = minutos

    def __repr__(self):
        return f"TipoServico({self.nome}, {self.minutos} min)"


def catalogo_padrao():
    return [
        TipoServico("Saque", 3),
        TipoServico("Depósito", 4),
        TipoServico("Pagamento de boleto", 5),
        TipoServico("Atendimento de cartão", 8),
        TipoServico("Abertura de conta", 15),
        TipoServico("Financiamento", 25),
    ]
