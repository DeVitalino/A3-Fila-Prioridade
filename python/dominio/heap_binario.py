class HeapBinario:
    # heap de mínimo guardado num vetor: filhos de i ficam em 2i+1 e 2i+2
    def __init__(self):
        self._itens = []

    def tamanho(self):
        return len(self._itens)

    def esta_vazio(self):
        return len(self._itens) == 0

    def itens(self):
        # cópia da lista, sem ordem garantida
        return list(self._itens)

    def espiar(self):
        if self.esta_vazio():
            raise IndexError("A fila está vazia")
        return self._itens[0]

    def inserir(self, cliente):
        self._itens.append(cliente)
        self._subir(len(self._itens) - 1)

    def remover(self):
        if self.esta_vazio():
            raise IndexError("A fila está vazia")
        return self._remover_indice(0)

    def remover_cliente(self, cliente):
        # busca linear, usada só pela cota rotativa
        for i, item in enumerate(self._itens):
            if item is cliente:
                return self._remover_indice(i)
        raise ValueError("Cliente não está na fila")

    def reorganizar(self):
        # chamado depois do aging, quando as chaves mudaram
        for i in range(len(self._itens) // 2 - 1, -1, -1):
            self._descer(i)

    def listar_ordenado(self):
        # só para exibição, não mexe no heap
        return sorted(self._itens, key=lambda c: c.chave())

    def _remover_indice(self, i):
        removido = self._itens[i]
        ultimo = self._itens.pop()
        if i < len(self._itens):
            self._itens[i] = ultimo
            self._subir(i)
            self._descer(i)
        return removido

    def _subir(self, i):
        while i > 0:
            pai = (i - 1) // 2
            if self._itens[i].chave() < self._itens[pai].chave():
                self._trocar(i, pai)
                i = pai
            else:
                break

    def _descer(self, i):
        n = len(self._itens)
        while True:
            menor = i
            esquerdo = 2 * i + 1
            direito = 2 * i + 2
            if esquerdo < n and self._itens[esquerdo].chave() < self._itens[menor].chave():
                menor = esquerdo
            if direito < n and self._itens[direito].chave() < self._itens[menor].chave():
                menor = direito
            if menor == i:
                break
            self._trocar(i, menor)
            i = menor

    def _trocar(self, a, b):
        self._itens[a], self._itens[b] = self._itens[b], self._itens[a]
