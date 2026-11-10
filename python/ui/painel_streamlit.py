import pandas as pd
import streamlit as st

from dominio.categoria import Categoria
from dominio.configuracao import Configuracao
from dominio.evento_fila import TipoEvento
from dominio.tipo_servico import catalogo_padrao
from repositorio.gerador_log_sql import GeradorLogSql
from repositorio.repositorio_atendimentos import RepositorioAtendimentos
from repositorio.repositorio_clientes import RepositorioClientes
from repositorio.repositorio_eventos import RepositorioEventos
from servico.gerador_clientes import GeradorClientes
from servico.metricas import Metricas
from servico.relogio_simulado import RelogioSimulado
from servico.servico_fila import ServicoFila


class PainelStreamlit:
    def __init__(self):
        st.set_page_config(page_title="Fila de Banco - A3", layout="wide")
        self.tipos = catalogo_padrao()
        if "servico" not in st.session_state:
            self.reiniciar(Configuracao(), 42)

    # ---------- estado da simulação ----------

    def reiniciar(self, config, semente):
        relogio = RelogioSimulado(config.data_base)
        repo_clientes = RepositorioClientes()
        repo_eventos = RepositorioEventos()
        repo_atendimentos = RepositorioAtendimentos()
        st.session_state.servico = ServicoFila(config, relogio, repo_clientes,
                                               repo_eventos, repo_atendimentos)
        st.session_state.gerador = GeradorClientes(self.tipos, semente)
        st.session_state.metricas = Metricas(repo_atendimentos, repo_eventos)
        st.session_state.gerador_sql = GeradorLogSql(relogio)

    # ---------- tela principal ----------

    def mostrar(self):
        st.title("Simulador de Fila de Banco")
        self.mostrar_configuracao()
        self.mostrar_controles()
        if st.session_state.get("automatico"):
            st.fragment(self.passo_automatico, run_every=1)()
        else:
            self.mostrar_paineis()

    def passo_automatico(self):
        servico = st.session_state.servico
        servico.avancar_tempo(1, st.session_state.gerador)
        self.mostrar_paineis()

    def mostrar_paineis(self):
        servico = st.session_state.servico
        st.subheader(f"Horário simulado: {servico.relogio.agora().strftime('%d/%m/%Y %H:%M')}")
        aba_fila, aba_guiches, aba_historico, aba_metricas, aba_eventos = st.tabs(
            ["Fila", "Guichês", "Histórico", "Métricas", "Alertas e starvation"])
        with aba_fila:
            self.mostrar_fila()
        with aba_guiches:
            self.mostrar_guiches()
        with aba_historico:
            self.mostrar_historico()
        with aba_metricas:
            self.mostrar_metricas()
        with aba_eventos:
            self.mostrar_eventos()

    # ---------- configuração (barra lateral) ----------

    def mostrar_configuracao(self):
        with st.sidebar:
            st.header("Configuração")
            qtd_guiches = st.number_input("Guichês", 1, 10, 3)
            semente_txt = st.text_input("Semente (vazio = aleatória)", "42")
            aging_ativo = st.checkbox("Aging ativo", True)
            minutos_por_nivel = st.number_input("Minutos de espera por nível de aging", 1, 120, 10)
            intervalo = st.number_input("Recalcular aging a cada (min)", 1, 60, 5)
            cota_ativa = st.checkbox("Cota rotativa ativa", True)
            cota_n = st.number_input("Prioritários seguidos antes de um comum (N)", 1, 20, 3)
            sla_prioritario = st.number_input("SLA prioritário (min)", 1, 240, 15)
            sla_vip = st.number_input("SLA VIP (min)", 1, 240, 10)
            sla_comum = st.number_input("SLA comum (min)", 1, 240, 30)
            limite = st.number_input("Limite de starvation (min)", 1, 480, 40)
            if st.button("Aplicar e reiniciar"):
                config = Configuracao(
                    qtd_guiches=int(qtd_guiches), aging_ativo=aging_ativo,
                    minutos_por_nivel=int(minutos_por_nivel), intervalo_recalculo=int(intervalo),
                    cota_ativa=cota_ativa, cota_n=int(cota_n),
                    sla={Categoria.PRIORITARIO: int(sla_prioritario),
                         Categoria.VIP: int(sla_vip), Categoria.COMUM: int(sla_comum)},
                    limite_starvation=int(limite))
                semente = int(semente_txt) if semente_txt.strip().isdigit() else None
                self.reiniciar(config, semente)
                st.rerun()
            st.checkbox("Modo automático (1 min simulado por segundo)", key="automatico")

    # ---------- controles ----------

    def mostrar_controles(self):
        servico = st.session_state.servico
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**Cliente manual**")
            categoria = st.selectbox("Categoria", list(Categoria), format_func=lambda c: c.descricao)
            tipo = st.selectbox("Serviço", self.tipos, format_func=lambda t: f"{t.nome} ({t.minutos} min)")
            if st.button("Gerar cliente"):
                servico.gerar_cliente(categoria, tipo)
        with col2:
            st.markdown("**Clientes aleatórios**")
            qtd = st.number_input("Quantidade", 1, 100, 5, key="qtd_aleatorios")
            if st.button("Gerar aleatórios"):
                for _ in range(int(qtd)):
                    cat, tp = st.session_state.gerador.sortear_cliente()
                    servico.gerar_cliente(cat, tp)
        with col3:
            st.markdown("**Avançar o tempo**")
            minutos = st.number_input("Minutos", 1, 240, 5, key="minutos_avanco")
            com_chegadas = st.checkbox("Com chegadas aleatórias", True)
            if st.button("Avançar"):
                gerador = st.session_state.gerador if com_chegadas else None
                servico.avancar_tempo(int(minutos), gerador)
        with col4:
            st.markdown("**Teste de estresse e logs**")
            qtd_estresse = st.number_input("Clientes no estresse", 10, 1000, 200)
            if st.button("Rodar teste de estresse"):
                servico.rodar_estresse(int(qtd_estresse), st.session_state.gerador)
            self.mostrar_exportacao()

    def mostrar_exportacao(self):
        servico = st.session_state.servico
        texto = st.session_state.gerador_sql.gerar(
            servico.guiches, servico.repo_eventos.listar(), servico.repo_atendimentos.listar())
        st.download_button("Exportar logs.sql", texto, file_name="logs.sql", mime="text/plain")

    # ---------- painéis ----------

    def mostrar_fila(self):
        servico = st.session_state.servico
        agora = servico.relogio.minuto_atual
        st.write(f"Clientes na fila: {servico.tamanho_fila()}")
        linhas = []
        for posicao, c in enumerate(servico.fila_ordenada(), start=1):
            linhas.append({
                "Posição": posicao,
                "Senha": c.senha,
                "Categoria": c.categoria.name,
                "Serviço": c.tipo_servico.nome,
                "Espera (min)": c.espera(agora),
                "Prioridade efetiva": c.prioridade_efetiva,
                "Situação": servico.situacao_sla(c),
            })
        if linhas:
            st.dataframe(pd.DataFrame(linhas), width="stretch", hide_index=True)
        else:
            st.info("Fila vazia")

    def mostrar_guiches(self):
        servico = st.session_state.servico
        agora = servico.relogio.minuto_atual
        colunas = st.columns(len(servico.guiches))
        for coluna, g in zip(colunas, servico.guiches):
            with coluna:
                st.markdown(f"**Guichê {g.numero}**")
                if g.esta_livre():
                    st.write("Livre")
                else:
                    st.write(f"Atendendo {g.cliente_atual.senha}")
                    st.write(f"Serviço: {g.cliente_atual.tipo_servico.nome}")
                    st.write(f"Termina em {g.minuto_fim - agora} min")
                st.write(f"Total atendidos: {g.total_atendidos}")

    def mostrar_historico(self):
        atendimentos = st.session_state.servico.repo_atendimentos.listar()
        if not atendimentos:
            st.info("Nenhum atendimento iniciado ainda")
            return
        linhas = []
        for a in reversed(atendimentos):
            linhas.append({
                "Senha": a.cliente.senha,
                "Categoria": a.cliente.categoria.name,
                "Guichê": a.id_guiche,
                "Início": st.session_state.servico.relogio.para_datetime(a.minuto_inicio).strftime("%H:%M"),
                "Espera (min)": a.tempo_espera,
                "SLA (min)": a.sla_minutos,
                "Status SLA": a.status_sla,
                "Chamada por": a.motivo,
            })
        st.dataframe(pd.DataFrame(linhas), width="stretch", hide_index=True)

    def mostrar_metricas(self):
        metricas = st.session_state.metricas
        maior, senha = metricas.maior_espera()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Atendidos", metricas.total_atendidos())
        c2.metric("Dentro do SLA", f"{metricas.percentual_dentro_sla():.1f}%")
        c3.metric("Maior espera", f"{maior} min ({senha})")
        c4.metric("Starvation detectado / evitado",
                  f"{metricas.starvation_detectados()} / {metricas.starvation_evitado()}")
        medias = metricas.tempo_medio_por_categoria()
        tabela = pd.DataFrame({
            "Categoria": [c.name for c in Categoria],
            "Tempo médio de espera (min)": [round(medias[c], 1) for c in Categoria],
            "% dentro do SLA": [round(metricas.percentual_dentro_sla(c), 1) for c in Categoria],
        })
        st.dataframe(tabela, width="stretch", hide_index=True)

    def mostrar_eventos(self):
        servico = st.session_state.servico
        eventos = [e for e in servico.repo_eventos.listar()
                   if e.tipo in (TipoEvento.ALERTA_SLA, TipoEvento.STARVATION)]
        if not eventos:
            st.info("Nenhum alerta de SLA ou starvation até agora")
            return
        linhas = []
        for e in reversed(eventos):
            linhas.append({
                "Horário": servico.relogio.para_datetime(e.minuto).strftime("%H:%M"),
                "Tipo": e.tipo.value,
                "Senha": e.cliente.senha,
                "Categoria": e.cliente.categoria.name,
                "Espera (min)": e.tempo_espera,
                "Detalhe": e.observacao,
            })
        st.dataframe(pd.DataFrame(linhas), width="stretch", hide_index=True)
