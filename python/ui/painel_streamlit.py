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
        st.set_page_config(
            page_title="Fila Prioritária | Simulador A3",
            page_icon="🏦",
            layout="wide",
            initial_sidebar_state="expanded",
        )
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
        st.markdown("""
        <style>
        .stApp { background: #f5f7fb; }
        [data-testid="stHeader"] { background: rgba(245,247,251,.92); }
        [data-testid="stSidebar"] { background: #111827; }
        [data-testid="stSidebar"] * { color: #f3f4f6; }
        [data-testid="stSidebar"] input, [data-testid="stSidebar"] [data-baseweb="select"] { color: #111827 !important; }
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: #e5e7eb !important; }
        .hero { padding: 1.35rem 1.6rem; border-radius: 18px; color: white;
                background: linear-gradient(115deg,#14213d 0%,#1d4ed8 65%,#0f766e 100%);
                margin: .2rem 0 1.2rem 0; box-shadow: 0 8px 24px rgba(30,64,175,.14); }
        .hero h1 { color: white; font-size: 1.8rem; margin: 0 0 .3rem 0; }
        .hero p { color: #dbeafe; margin: 0; font-size: .95rem; }
        div[data-testid="stMetric"] { background: white; border: 1px solid #e7ebf2;
                padding: 14px 16px; border-radius: 14px; box-shadow: 0 2px 8px rgba(15,23,42,.035); }
        div[data-testid="stTabs"] button { font-weight: 600; }
        div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
        div.stButton > button, div.stDownloadButton > button { border-radius: 10px; font-weight: 600; min-height: 2.6rem; }
        div[data-testid="stVerticalBlock"] > div:has(> div > .control-card) { gap: .4rem; }
        </style>
        <div class="hero">
          <h1>🏦 Central de Atendimento</h1>
          <p>Simulador de filas com quatro níveis de prioridade, envelhecimento e acompanhamento de SLA.</p>
        </div>
        """, unsafe_allow_html=True)
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
        
        # 3 abas: Filas+Atendimentos, Guichês, Indicadores
        aba_filas, aba_guiches, aba_indicadores = st.tabs([
            "📋 Fila e Atendimentos",
            "🪟 Guichês",
            "📈 Indicadores e Auditoria"
        ])
        
        with aba_filas:
            # Fila de pessoas aguardando
            self.mostrar_duas_filas()
            # Separador visual
            st.divider()
            # Histórico de atendimentos logo abaixo
            self.mostrar_historico()
            
        with aba_guiches:
            self.mostrar_guiches()
            
        with aba_indicadores:
            self.mostrar_metricas()
            st.divider()
            self.mostrar_eventos()
            st.divider()
            self.mostrar_exportacao()

    # ---------- configuração (barra lateral) ----------

    def mostrar_configuracao(self):
        with st.sidebar:
            st.markdown("## ⚙️ Configurações")
            st.caption("Defina as regras antes de iniciar uma nova simulação.")
            qtd_guiches = st.number_input("Quantidade de guichês", 1, 10, 3, key="cfg_guiches")
            semente_txt = st.text_input("Semente aleatória (opcional)", "42", key="cfg_semente")

            st.divider()
            with st.expander("🧭 Envelhecimento da fila", expanded=False):
                st.caption("O envelhecimento aumenta a prioridade de quem espera há mais tempo.")
                aging_ativo = st.checkbox("Ativar envelhecimento", True, key="cfg_aging")
                intervalo = st.number_input("Recalcular a cada (minutos)", 1, 60, 5, key="cfg_intervalo")
                st.info("Regra atual do algoritmo: multiplicador de 1,6x a cada 20 minutos. O nível 4 mantém prioridade absoluta.")

            with st.expander("🔄 Cota rotativa", expanded=False):
                st.caption("Evita que pessoas sem prioridade especial aguardem indefinidamente.")
                cota_ativa = st.checkbox("Ativar cota rotativa", True, key="cfg_cota")
                cota_n = st.number_input("Prioritários antes de chamar 1 comum", 1, 20, 3, key="cfg_cota_n")

            st.markdown("### ⏱️ Tempo máximo de espera")
            st.caption("Configure o limite de espera na fila (SLA) de cada grupo. Os quatro valores podem ser alterados independentemente. Esse limite mede a espera até ser chamado, não a duração do serviço no guichê.")
            sla_n4 = st.number_input("Nível 4 · 80 anos ou mais (min)", 1, 480, 10, key="cfg_sla_n4", help="Tempo máximo de espera previsto para pessoas com 80 anos ou mais.")
            sla_n3 = st.number_input("Nível 3 · 60 a 79 anos (min)", 1, 480, 15, key="cfg_sla_n3")
            sla_n2 = st.number_input("Nível 2 · Pessoa com deficiência (min)", 1, 480, 20, key="cfg_sla_n2")
            sla_n1 = st.number_input("Nível 1 · Sem prioridade especial (min)", 1, 480, 30, key="cfg_sla_n1")
            st.caption(f"Resumo configurado: N4 {sla_n4} min · N3 {sla_n3} min · N2 {sla_n2} min · N1 {sla_n1} min")
            limite = st.number_input("Limite para detectar espera excessiva (min)", 1, 720, 40, key="cfg_limite")

            st.divider()
            if st.button("✨ Aplicar configurações e reiniciar", type="primary", use_container_width=True):
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
                        Categoria.NIVEL_1: int(sla_n1),
                    },
                    limite_starvation=int(limite),
                )
                semente = int(semente_txt) if semente_txt.strip().isdigit() else None
                self.reiniciar(config, semente)
                st.session_state.automatico = False
                st.success("Configurações aplicadas. Simulação reiniciada.")
                st.rerun()

            st.checkbox("🚀 Modo automático (1 min por segundo)", key="automatico")

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
                st.rerun()
        
        with col2:
            st.markdown("**🎲 Clientes aleatórios**")
            qtd = st.number_input("Quantidade", 1, 500, 5, key="qtd_aleatorios")
            st.caption("Distribuição: 1% N4, 12% N3, 10% N2, 77% N1")
            if st.button("🎲 Gerar aleatórios"):
                quantidade_solicitada = int(qtd)
                # Gerar TODOS os clientes primeiro (sem alocar a guichês)
                for i in range(quantidade_solicitada):
                    cat, idade, tp = st.session_state.gerador.sortear_cliente()
                    # Usar _entrar_na_fila ao invés de gerar_cliente para não chamar _chamar_proximos
                    servico._entrar_na_fila(cat, tp, idade)
                # AGORA sim chamar para alocar aos guichês disponíveis
                servico._chamar_proximos()
                st.rerun()
        
        with col3:
            st.markdown("**⏩ Avançar o tempo**")
            minutos = st.number_input("Minutos", 1, 240, 5, key="minutos_avanco")
            com_chegadas = st.checkbox("Com chegadas aleatórias", True)
            if st.button("⏩ Avançar"):
                gerador = st.session_state.gerador if com_chegadas else None
                servico.avancar_tempo(int(minutos), gerador)
                st.rerun()
        
        with col4:
            st.markdown("**🧪 Teste de estresse**")
            qtd_estresse = st.number_input("Clientes no estresse", 10, 1000, 200)
            if st.button("🧪 Rodar teste"):
                servico.rodar_estresse(int(qtd_estresse), st.session_state.gerador)
                st.rerun()

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
        """Mostra a fila de clientes aguardando."""
        servico = st.session_state.servico
        agora = servico.relogio.minuto_atual
        
        st.markdown("### 📋 Pessoas aguardando: " + str(servico.tamanho_fila()))
        
        if servico.tamanho_fila() == 0:
            st.info("✓ Fila vazia - todos já foram atendidos")
            return
        
        # Fila de chegada (única lista)
        st.markdown("#### 📋 Ordem de Chegada")
        st.caption("Sequência cronológica de entrada na fila")
        
        fila_chegada = servico.fila_por_chegada()
        linhas_chegada = []
        for posicao, c in enumerate(fila_chegada, start=1):
            hora_chegada = servico.relogio.para_datetime(c.minuto_chegada).strftime("%H:%M")
            emoji = "👑" if c.categoria == Categoria.NIVEL_4 else ""
            
            linhas_chegada.append({
                "Ordem": posicao,
                "Senha": f"{emoji}{c.senha}",
                "Nível": c.categoria.nome_curto,
                "Idade": f"{c.idade}a",
                "Serviço": c.tipo_servico.nome,
                "Chegada": hora_chegada,
                "Tempo Serv.": f"{c.tipo_servico.minutos} min",
                "SLA": f"{servico.config.sla[c.categoria]} min",
                "Situação": "Aguardando"
            })
        
        if linhas_chegada:
            df_chegada = pd.DataFrame(linhas_chegada)
            st.dataframe(df_chegada, use_container_width=True, hide_index=True, height=400)

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
