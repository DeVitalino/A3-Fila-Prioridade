class RepositorioEventos:
    def __init__(self):
        self._eventos = []

    def adicionar(self, evento):
        evento.id_evento = len(self._eventos) + 1
        self._eventos.append(evento)

    def listar(self):
        return list(self._eventos)

    def listar_por_tipo(self, tipo):
        return [e for e in self._eventos if e.tipo == tipo]
