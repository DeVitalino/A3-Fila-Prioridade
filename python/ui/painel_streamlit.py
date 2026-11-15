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
        st.set_page_config(page_title="Simulador Fila Bancária - A3", layout="wide")
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
        st.title("🏦 Simulador de Fila Bancária - Sistema de 4 Níveis de Prioridade")
        st.caption("Projeto A3 - Estrutura de Dados: Filas de Prioridade com Envelhecimento")
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
        st.subheader(f"⏰ Horário simulado: {servico.relogio.agora().strftime('%d/%m/%Y %H:%M')}")
        
        # 4 abas reorganizadas
        aba_filas, aba_guiches, aba_atendimentos, aba_indicadores = st.tabs([
            "📋 Filas",
            "🪟 Guichês",
            "📊 Atendimentos",
            "📈 Indicadores e Auditoria"
        ])
        
        with aba_filas:
            self.mostrar_duas_filas()
        with aba_guiches:
            self.mostrar_guiches()
        with aba_atendimentos:
            self.mostrar_historico()
        with aba_indicadores:
            self.mostrar_metricas()
            st.divider()
            self.mostrar_eventos()
            st.divider()
            self.mostrar_exportacao()

    # ---------- configuração (barra lateral) ----------

    def mostrar_configuracao(self):
        with st.sidebar:
            st.header("⚙️ Configuração")
            qtd_guiches = st.number_input("Guichês", 1, 10, 3)
            semente_txt = st.text_input("Semente (vazio = aleatória)", "42")
            
            st.subheader("Envelhecimento (Fixo)")
            st.info("✓ Multiplicador: 1.6x a cada 20 minutos\n✓ NÍVEL 4 (80+): prioridade absoluta")
            aging_ativo = st.checkbox("Envelhecimento ativo", True)
            intervalo = st.number_input("Recalcular a cada (min)", 1, 60, 5)
            
            st.subheader("Cota Rotativa")
            cota_ativa = st.checkbox("Cota rotativa ativa", True)
            cota_n = st.number_input("Prioritários seguidos antes de 1 comum (N)", 1, 20, 3)
            
            st.subheader("SLA por Nível")
            st.caption("SLA = Tempo máximo de espera tolerado")
            sla_n4 = st.number_input("SLA Nível 4 (80+) - min", 1, 240, 10)
            sla_n3 = st.number_input("SLA Nível 3 (60-79) - min", 1, 240, 15)
            sla_n2 = st.number_input("SLA Nível 2 (PCD) - min", 1, 240, 20)
            sla_n1 = st.number_input("SLA Nível 1 (Comum) - min", 1, 240, 30)
            limite = st.number_input("Limite de starvation (min)", 1, 480, 40)
            
            if st.button("✨ Aplicar e reiniciar"):
                config = Configuracao(
                    qtd_guiches=int(qtd_guiches),
                    aging_ativo=aging_ativo,
                    intervalo_recalculo=int(intervalo),
                    cota_ativa=cota_ativa,
                    cota_n=int(cota_n),
                    sla={
                        Categoria.NIVEL_4: int(sla_n4),
                        Categoria.NIVEL_3: int(sla_n3),
                        Categoria.NIVEL_2: int(sla_n2),
                        Categoria.NIVEL_1: int(sla_n1)
                    },
                    limite_starvation=int(limite))
                semente = int(semente_txt) if semente_txt.strip().isdigit() else None
                self.reiniciar(config, semente)
                st.rerun()
            
            st.checkbox("🚀 Modo automático (1 min/segundo)", key="automatico")

    # ---------- controles ----------

    def mostrar_controles(self):
        servico = st.session_state.servico
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**👤 Cliente manual**")
            categoria = st.selectbox("Nível de prioridade", list(Categoria), 
                                    format_func=lambda c: c.descricao)
            tipo = st.selectbox("Serviço", self.tipos, 
                              format_func=lambda t: f"{t.nome} ({t.minutos} min)")
            if st.button("➕ Gerar cliente"):
                servico.gerar_cliente(categoria, tipo)
        
        with col2:
            st.markdown("**🎲 Clientes aleatórios**")
            qtd = st.number_input("Quantidade", 1, 100, 5, key="qtd_aleatorios")
            st.caption("Distribuição: 1% N4, 12% N3, 10% N2, 77% N1")
            if st.button("🎲 Gerar aleatórios"):
                for _ in range(int(qtd)):
                    cat, idade, tp = st.session_state.gerador.sortear_cliente()
                    servico.gerar_cliente(cat, tp, idade)
        
        with col3:
            st.markdown("**⏩ Avançar o tempo**")
            minutos = st.number_input("Minutos", 1, 240, 5, key="minutos_avanco")
            com_chegadas = st.checkbox("Com chegadas aleatórias", True)
            if st.button("⏩ Avançar"):
                gerador = st.session_state.gerador if com_chegadas else None
                servico.avancar_tempo(int(minutos), gerador)
        
        with col4:
            st.markdown("**🧪 Teste de estresse**")
            qtd_estresse = st.number_input("Clientes no estresse", 10, 1000, 200)
            if st.button("🧪 Rodar teste"):
                servico.rodar_estresse(int(qtd_estresse), st.session_state.gerador)

    def mostrar_exportacao(self):
        servico = st.session_state.servico
        st.subheader("💾 Exportar Auditoria SQL")
        texto = st.session_state.gerador_sql.gerar(
            servico.guiches, servico.repo_eventos.listar(), servico.repo_atendimentos.listar())
        st.download_button(
            "⬇️ Baixar logsA3.sql",
            texto,
            file_name="logsA3.sql",
            mime="text/plain",
            help="Arquivo SQL com todos os eventos e atendimentos"
        )

    # ---------- painéis ----------

    def mostrar_duas_filas(self):
        """Mostra as duas listas: ordem de chegada e ordem calculada."""
        servico = st.session_state.servico
        agora = servico.relogio.minuto_atual
        
        st.markdown("### 📋 Pessoas aguardando: " + str(servico.tamanho_fila()))
        
        if servico.tamanho_fila() == 0:
            st.info("✓ Fila vazia - todos já foram atendidos")
            return
        
        col_chegada, col_calculada = st.columns(2)
        
        # LISTA 1: Ordem de chegada (cronológica)
        with col_chegada:
            st.markdown("#### 1️⃣ Ordem de Chegada")
            st.caption("Sequência cronológica de entrada na fila")
            
            fila_chegada = servico.fila_por_chegada()
            linhas_chegada = []
            for posicao, c in enumerate(fila_chegada, start=1):
                linhas_chegada.append({
                    "Pos": posicao,
                    "Senha": c.senha,
                    "Nível": c.categoria.nome_curto,
                    "Idade": f"{c.idade}a",
                    "Serviço": c.tipo_servico.nome,
                    "Espera": f"{c.espera(agora)} min",
                    "Pontuação": f"{c.pontuacao_atual:.2f}",
                    "SLA": servico.situacao_sla(c)
                })
            
            if linhas_chegada:
                df_chegada = pd.DataFrame(linhas_chegada)
                st.dataframe(df_chegada, use_container_width=True, hide_index=True, height=400)
        
        # LISTA 2: Ordem calculada (heap/prioridade)
        with col_calculada:
            st.markdown("#### 2️⃣ Ordem de Atendimento (Calculada)")
            st.caption("Ordenada por prioridade + envelhecimento - próximos a serem chamados")
            
            fila_ordenada = servico.fila_ordenada()
            linhas_ordenada = []
            for posicao, c in enumerate(fila_ordenada, start=1):
                # Destacar NIVEL_4
                emoji = "👑" if c.categoria == Categoria.NIVEL_4 else ""
                linhas_ordenada.append({
                    "Pos": posicao,
                    "Senha": f"{emoji}{c.senha}",
                    "Nível": c.categoria.nome_curto,
                    "Idade": f"{c.idade}a",
                    "Serviço": c.tipo_servico.nome,
                    "Espera": f"{c.espera(agora)} min",
                    "Pontuação": f"{c.pontuacao_atual:.2f}",
                    "SLA": servico.situacao_sla(c)
                })
            
            if linhas_ordenada:
                df_ordenada = pd.DataFrame(linhas_ordenada)
                st.dataframe(df_ordenada, use_container_width=True, hide_index=True, height=400)

    def mostrar_guiches(self):
        servico = st.session_state.servico
        agora = servico.relogio.minuto_atual
        
        st.markdown("### 🪟 Status dos Guichês")
        colunas = st.columns(len(servico.guiches))
        
        for coluna, g in zip(colunas, servico.guiches):
            with coluna:
                if g.esta_livre():
                    st.success(f"**Guichê {g.numero}**\n\n✓ Livre")
                else:
                    st.info(f"**Guichê {g.numero}**\n\n"
                           f"👤 {g.cliente_atual.senha}\n"
                           f"📋 {g.cliente_atual.tipo_servico.nome}\n"
                           f"⏱️ Termina em {g.minuto_fim - agora} min")
                st.caption(f"Total: {g.total_atendidos} atendimentos")

    def mostrar_historico(self):
        st.markdown("### 📊 Histórico de Atendimentos")
        atendimentos = st.session_state.servico.repo_atendimentos.listar()
        
        if not atendimentos:
            st.info("Nenhum atendimento realizado ainda")
            return
        
        # Dicionário para traduzir motivos
        traducao_motivo = {
            "NORMAL": "NORMAL",
            "AGING": "ENVELHECIMENTO",
            "COTA": "COTA"
        }
        
        linhas = []
        # Enumerar para obter ordem cronológica de chegada
        for ordem, a in enumerate(reversed(atendimentos), start=1):
            emoji = "👑" if a.cliente.categoria == Categoria.NIVEL_4 else ""
            
            # Calcular tempo de atendimento (duração no guichê)
            tempo_atendimento = a.minuto_fim - a.minuto_inicio
            
            # Horários formatados
            hora_chegada = st.session_state.servico.relogio.para_datetime(a.cliente.minuto_chegada).strftime("%H:%M")
            hora_chamado = st.session_state.servico.relogio.para_datetime(a.minuto_inicio).strftime("%H:%M")
            
            linhas.append({
                "Ordem": len(atendimentos) - ordem + 1,  # Ordem cronológica (1, 2, 3...)
                "Senha": f"{emoji}{a.cliente.senha}",
                "Nível": a.cliente.categoria.nome_curto,
                "Idade": f"{a.cliente.idade}a",
                "Serviço": a.cliente.tipo_servico.nome,
                "Chegada": hora_chegada,
                "Chamado": hora_chamado,
                "Espera": f"{a.tempo_espera} min",
                "Atendimento": f"{tempo_atendimento} min",
                "Guichê": a.id_guiche,
                "SLA": f"{a.sla_minutos} min",
                "Status": a.status_sla,
                "Motivo": traducao_motivo.get(a.motivo, a.motivo)
            })
        
        df = pd.DataFrame(linhas)
        st.dataframe(df, use_container_width=True, hide_index=True, height=400)

    def mostrar_metricas(self):
        st.markdown("### 📈 Indicadores Gerais")
        metricas = st.session_state.metricas
        maior, senha = metricas.maior_espera()
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("✅ Atendidos", metricas.total_atendidos())
        c2.metric("📊 Dentro do SLA", f"{metricas.percentual_dentro_sla():.1f}%")
        c3.metric("⏱️ Maior espera", f"{maior} min ({senha})")
        c4.metric("⚠️ Starvation", f"{metricas.starvation_detectados()} / {metricas.starvation_evitado()}")
        
        st.markdown("#### Tempo médio por nível")
        medias = metricas.tempo_medio_por_categoria()
        tabela = pd.DataFrame({
            "Nível": [c.nome_curto for c in Categoria],
            "Tempo médio (min)": [round(medias[c], 1) for c in Categoria],
            "% dentro do SLA": [round(metricas.percentual_dentro_sla(c), 1) for c in Categoria]
        })
        st.dataframe(tabela, use_container_width=True, hide_index=True)

    def mostrar_eventos(self):
        st.markdown("### ⚠️ Alertas de SLA e Starvation")
        servico = st.session_state.servico
        eventos = [e for e in servico.repo_eventos.listar()
                   if e.tipo in (TipoEvento.ALERTA_SLA, TipoEvento.STARVATION)]
        
        if not eventos:
            st.success("✓ Nenhum alerta crítico detectado")
            return
        
        linhas = []
        for e in reversed(eventos):
            emoji = "⚠️" if e.tipo == TipoEvento.ALERTA_SLA else "🚨"
            linhas.append({
                "": emoji,
                "Horário": servico.relogio.para_datetime(e.minuto).strftime("%H:%M"),
                "Tipo": e.tipo.value,
                "Senha": e.cliente.senha,
                "Nível": e.cliente.categoria.nome_curto,
                "Espera": f"{e.tempo_espera} min",
                "Detalhe": e.observacao
            })
        
        df = pd.DataFrame(linhas)
        st.dataframe(df, use_container_width=True, hide_index=True, height=300)
