class RepositorioAtendimentos:
    def __init__(self):
        self._atendimentos = []

    def adicionar(self, atendimento):
        atendimento.id_atendimento = len(self._atendimentos) + 1
        self._atendimentos.append(atendimento)

    def listar(self):
        return list(self._atendimentos)

    def listar_por_categoria(self, categoria):
        return [a for a in self._atendimentos if a.cliente.categoria == categoria]
