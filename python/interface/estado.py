"""Criação e recuperação do estado da simulação."""
import streamlit as st
from dominio.configuracao import Configuracao
from repositorio.repositorio_atendimentos import RepositorioAtendimentos
from repositorio.repositorio_clientes import RepositorioClientes
from repositorio.repositorio_eventos import RepositorioEventos
from repositorio.gerador_log_sql import GeradorLogSql
from servico.gerador_clientes import GeradorClientes
from servico.metricas import Metricas
from servico.relogio_simulado import RelogioSimulado
from servico.servico_fila import ServicoFila
from dominio.tipo_servico import catalogo_padrao
from dominio.categoria import Categoria

def reiniciar(config=None, semente=42):
    config = config or Configuracao()
    relogio=RelogioSimulado(config.data_base)
    rc,re,ra=RepositorioClientes(),RepositorioEventos(),RepositorioAtendimentos()
    st.session_state["servico"]=ServicoFila(config,relogio,rc,re,ra)
    st.session_state["gerador"]=GeradorClientes(catalogo_padrao(),semente)
    st.session_state["metricas"]=Metricas(ra,re)
    st.session_state["gerador_sql"]=GeradorLogSql(relogio)

def garantir_estado():
    if "servico" not in st.session_state:
        reiniciar()
    st.session_state.setdefault("automatico",False)
    st.session_state.setdefault("pagina","📊 Painel")
