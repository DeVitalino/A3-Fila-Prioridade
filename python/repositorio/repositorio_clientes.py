class RepositorioClientes:
    def __init__(self):
        self._clientes = []

    def proximo_id(self):
        return len(self._clientes) + 1

    def adicionar(self, cliente):
        self._clientes.append(cliente)

    def listar(self):
        return list(self._clientes)

    def buscar_por_senha(self, senha):
        for cliente in self._clientes:
            if cliente.senha == senha:
                return cliente
        return None
