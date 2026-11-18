"""Entrada do Streamlit. Execute com: streamlit run trabalhoA3.py"""
import streamlit as st

st.set_page_config(page_title="Fila Justa | Simulador A3",page_icon="🏦",layout="wide",initial_sidebar_state="expanded")

from interface import paginas
from interface.estado import garantir_estado

PAGINAS={
    "📊 Painel":paginas.pagina_painel,
    "📋 Filas":paginas.pagina_filas,
    "🪟 Guichês":paginas.pagina_guiches,
    "🧾 Atendimentos":paginas.pagina_atendimentos,
    "📈 Indicadores":paginas.pagina_indicadores,
}

def _painel_automatico():
    st.session_state.servico.avancar_tempo(1,st.session_state.gerador)
    paginas.pagina_painel()

def main():
    garantir_estado()
    paginas.injetar_css()
    paginas.cabecalho()
    paginas.barra_lateral()
    # O controle fica fora do fragmento para evitar que a frequência seja recalculada incorretamente.
    st.toggle("🚀 Modo automático — 1 minuto simulado por segundo",key="automatico")
    escolhida=st.radio("Navegação",list(PAGINAS),horizontal=True,label_visibility="collapsed",key="pagina")
    if escolhida=="📊 Painel" and st.session_state.get("automatico"):
        st.fragment(run_every=1.0)(_painel_automatico)()
    else:
        PAGINAS[escolhida]()

if __name__=="__main__":
    main()
