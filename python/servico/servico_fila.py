from dominio.atendimento import Atendimento
from dominio.categoria import Categoria
from dominio.cliente import Cliente
from dominio.evento_fila import EventoFila, TipoEvento
from dominio.guiche import Guiche
from dominio.heap_binario import HeapBinario


class ServicoFila:
    def __init__(self, config, relogio, repo_clientes, repo_eventos, repo_atendimentos):
        config.validar()
        self.config = config
        self.relogio = relogio
        self.repo_clientes = repo_clientes
        self.repo_eventos = repo_eventos
        self.repo_atendimentos = repo_atendimentos
        self.heap = HeapBinario()
        self.guiches = [Guiche(i + 1) for i in range(config.qtd_guiches)]
        self.prioritarios_seguidos = 0
        self.contador_senha = {categoria: 0 for categoria in Categoria}

    # ---------- entrada de clientes ----------

    def gerar_cliente(self, categoria, tipo_servico, idade=None):
        """
        Gera um cliente e adiciona na fila.
        Se idade não for fornecida, gera compatível com a categoria.
        """
        if idade is None:
            # Gerar idade compatível com a categoria
            if categoria == Categoria.NIVEL_4:
                import random
                idade = random.randint(80, 95)
            elif categoria == Categoria.NIVEL_3:
                import random
                idade = random.randint(60, 79)
            elif categoria == Categoria.NIVEL_2:
                import random
                idade = random.randint(18, 70)
            else:  # NIVEL_1
                import random
                idade = random.randint(18, 59)
        
        cliente = self._entrar_na_fila(categoria, tipo_servico, idade)
        self._chamar_proximos()
        return cliente

    def _entrar_na_fila(self, categoria, tipo_servico, idade):
        self.contador_senha[categoria] += 1
        senha = f"{categoria.prefixo_senha}{self.contador_senha[categoria]:03d}"
        cliente = Cliente(
            self.repo_clientes.proximo_id(),
            senha,
            categoria,
            tipo_servico,
            self.relogio.minuto_atual,
            idade
        )
        self.repo_clientes.adicionar(cliente)
        self.heap.inserir(cliente)
        self.repo_eventos.adicionar(
            EventoFila(TipoEvento.ENTRADA, self.relogio.minuto_atual, cliente))
        return cliente

    # ---------- passagem do tempo ----------

    def avancar_tempo(self, minutos, gerador=None):
        if minutos < 1:
            raise ValueError("Informe pelo menos 1 minuto")
        for _ in range(minutos):
            novos = gerador.chegadas_no_minuto() if gerador else []
            self._passar_um_minuto(novos)

    def rodar_estresse(self, quantidade, gerador):
        if quantidade < 1:
            raise ValueError("A quantidade de clientes deve ser maior que zero")
        restantes = quantidade
        while restantes > 0:
            novos = gerador.chegadas_no_minuto()[:restantes]
            restantes -= len(novos)
            self._passar_um_minuto(novos)
        while not self._tudo_vazio():
            self._passar_um_minuto([])

    def _tudo_vazio(self):
        return self.heap.esta_vazio() and all(g.esta_livre() for g in self.guiches)

    def _passar_um_minuto(self, novos):
        self.relogio.avancar(1)
        self._finalizar_atendimentos()
        for categoria, idade, tipo in novos:
            self._entrar_na_fila(categoria, tipo, idade)
        self._aplicar_aging()
        self._verificar_alertas()
        self._chamar_proximos()

    def _finalizar_atendimentos(self):
        for guiche in self.guiches:
            if not guiche.esta_livre() and guiche.minuto_fim <= self.relogio.minuto_atual:
                guiche.liberar()

    # ---------- aging com multiplicador 1.6 ----------

    def _aplicar_aging(self):
        """
        Aplica o novo algoritmo de aging:
        - A cada 20 minutos COMPLETOS, multiplica pontuação por 1.6
        - NIVEL_4 (80+) mantém prioridade absoluta (não entra no cálculo)
        """
        if not self.config.aging_ativo:
            return
        
        # Recalcular a cada intervalo configurado (5 min padrão)
        if self.relogio.minuto_atual % self.config.intervalo_recalculo != 0:
            return
        
        agora = self.relogio.minuto_atual
        for cliente in self.heap.itens():
            # Atualizar pontuação baseada no aging
            cliente.calcular_pontuacao(agora)
        
        # Reorganizar heap com novas pontuações
        self.heap.reorganizar()

    # ---------- SLA e starvation ----------

    def _verificar_alertas(self):
        agora = self.relogio.minuto_atual
        for cliente in self.heap.itens():
            espera = cliente.espera(agora)
            sla = self.config.sla[cliente.categoria]
            if not cliente.alerta_sla_emitido and espera >= sla * self.config.percentual_alerta_sla:
                cliente.alerta_sla_emitido = True
                self.repo_eventos.adicionar(EventoFila(
                    TipoEvento.ALERTA_SLA, agora, cliente, tempo_espera=espera,
                    observacao=f"perto de estourar o SLA de {sla} min"))
            if not cliente.starvation_detectado and espera >= self.config.limite_starvation:
                cliente.starvation_detectado = True
                self.repo_eventos.adicionar(EventoFila(
                    TipoEvento.STARVATION, agora, cliente, tempo_espera=espera,
                    observacao=f"espera passou de {self.config.limite_starvation} min"))

    def situacao_sla(self, cliente):
        espera = cliente.espera(self.relogio.minuto_atual)
        sla = self.config.sla[cliente.categoria]
        if espera > sla:
            return "SLA estourado"
        if espera >= sla * self.config.percentual_alerta_sla:
            return "Perto do SLA"
        return "Dentro do SLA"

    # ---------- chamada para os guichês ----------

    def _chamar_proximos(self):
        for guiche in self.guiches:
            if self.heap.esta_vazio():
                return
            if guiche.esta_livre():
                self._atender_proximo(guiche)

    def _atender_proximo(self, guiche):
        cliente, motivo = self._escolher_proximo()
        if motivo == "COTA":
            self.heap.remover_cliente(cliente)
        else:
            self.heap.remover()
        self._iniciar_atendimento(cliente, guiche, motivo)

    def _escolher_proximo(self):
        """
        Escolhe próximo cliente considerando:
        1. NIVEL_4 sempre tem prioridade absoluta
        2. Cota rotativa (se ativa)
        3. Aging (pontuação aumentada)
        """
        if self.config.cota_ativa and self.prioritarios_seguidos >= self.config.cota_n:
            comum = self._comum_mais_antigo()
            if comum is not None:
                return comum, "COTA"
        
        primeiro = self.heap.espiar()
        
        # Verificar se foi beneficiado pelo aging
        if primeiro.pontuacao_atual > primeiro.pontuacao_inicial:
            return primeiro, "AGING"
        
        return primeiro, "NORMAL"

    def _comum_mais_antigo(self):
        """Busca o cliente NIVEL_1 mais antigo na fila."""
        comuns = [c for c in self.heap.itens() if c.categoria == Categoria.NIVEL_1]
        if not comuns:
            return None
        return min(comuns, key=lambda c: c.chave())

    def _iniciar_atendimento(self, cliente, guiche, motivo):
        agora = self.relogio.minuto_atual
        sla = self.config.sla[cliente.categoria]
        guiche.iniciar(cliente, agora)
        atendimento = Atendimento(cliente, guiche.numero, agora, sla, motivo)
        self.repo_atendimentos.adicionar(atendimento)
        self.repo_eventos.adicionar(EventoFila(
            TipoEvento.SAIDA, agora, cliente, id_guiche=guiche.numero,
            tempo_espera=atendimento.tempo_espera, status_sla=atendimento.status_sla,
            observacao=f"chamada por {motivo}"))
        self._atualizar_cota(cliente)

    def _atualizar_cota(self, cliente):
        """Atualiza contador de cota. NIVEL_3 e NIVEL_4 contam como prioritários."""
        if cliente.categoria in (Categoria.NIVEL_3, Categoria.NIVEL_4):
            self.prioritarios_seguidos += 1
        elif cliente.categoria == Categoria.NIVEL_1:
            self.prioritarios_seguidos = 0

    # ---------- consultas para a interface ----------

    def fila_ordenada(self):
        """Retorna fila ordenada pela pontuação (ordem de atendimento)."""
        return self.heap.listar_ordenado()
    
    def fila_por_chegada(self):
        """
        Retorna fila na ordem de chegada (cronológica).
        Mostra apenas clientes que ainda estão aguardando.
        """
        # IDs dos clientes que já foram atendidos
        atendidos_ids = {a.cliente.id_cliente for a in self.repo_atendimentos.listar()}
        
        # Filtrar apenas os que ainda estão na fila
        aguardando = [c for c in self.repo_clientes.listar() 
                      if c.id_cliente not in atendidos_ids]
        
        # Ordenar por ID (ordem de chegada)
        return sorted(aguardando, key=lambda c: c.id_cliente)

    def tamanho_fila(self):
        return self.heap.tamanho()
