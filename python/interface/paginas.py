"""Telas do simulador. A lógica de negócio permanece nos módulos dominio/servico."""
import pandas as pd
import streamlit as st
from dominio.categoria import Categoria
from dominio.configuracao import Configuracao
from dominio.evento_fila import TipoEvento
from dominio.tipo_servico import catalogo_padrao
from . import componentes as comp
from .estilo import CSS
from .estado import reiniciar

def _html(codigo):
    st.markdown(codigo, unsafe_allow_html=True)

def injetar_css():
    _html(f"<style>{CSS}</style>")

def cabecalho():
    _html(comp.hero("🏦 Fila Justa", "Simulador de atendimento com prioridades, envelhecimento da fila e acompanhamento de SLA.",
                    ["Python · POO", "Heap Binário", "Streamlit", "Auditoria SQL"]))

def barra_lateral():
    serv=st.session_state.servico
    cfg=serv.config
    with st.sidebar:
        st.header("⚙️ Parâmetros")
        st.caption("As alterações são aplicadas ao reiniciar a simulação.")
        with st.expander("🪟 Estrutura de atendimento", expanded=True):
            guiches=st.number_input("Quantidade de guichês",1,10,int(cfg.qtd_guiches),key="cfg_guiches")
            semente=st.text_input("Semente aleatória",str(st.session_state.get("semente_atual",42)),key="cfg_semente")
        with st.expander("🧭 Envelhecimento (aging)"):
            aging=st.checkbox("Ativar aging",bool(cfg.aging_ativo),key="cfg_aging")
            intervalo=st.number_input("Intervalo de recálculo (min)",1,60,int(cfg.intervalo_recalculo),key="cfg_intervalo")
            st.info("A pontuação cresce 1,6x a cada período completo de 20 minutos. O Nível 4 mantém prioridade absoluta.")
        with st.expander("🔄 Cota rotativa"):
            cota=st.checkbox("Ativar cota rotativa",bool(cfg.cota_ativa),key="cfg_cota")
            cota_n=st.number_input("Prioritários antes de chamar 1 comum",1,20,int(cfg.cota_n),key="cfg_cota_n")
        with st.expander("⏱️ Limites de espera (SLA)"):
            n4=st.number_input("Nível 4 · 80+ anos (min)",1,480,int(cfg.sla[Categoria.NIVEL_4]),key="cfg_sla_n4")
            n3=st.number_input("Nível 3 · 60–79 anos (min)",1,480,int(cfg.sla[Categoria.NIVEL_3]),key="cfg_sla_n3")
            n2=st.number_input("Nível 2 · PCD (min)",1,480,int(cfg.sla[Categoria.NIVEL_2]),key="cfg_sla_n2")
            n1=st.number_input("Nível 1 · Comum (min)",1,480,int(cfg.sla[Categoria.NIVEL_1]),key="cfg_sla_n1")
            limite=st.number_input("Limite para espera excessiva (min)",1,720,int(cfg.limite_starvation),key="cfg_limite")
        with st.expander("🖥️ Exibição"):
            st.slider("Cartões por lista",3,30,8,key="cfg_limite_cartoes")
        if st.button("Aplicar e reiniciar simulação",type="primary",key="aplicar_config"):
            try:
                config=Configuracao(qtd_guiches=int(guiches),aging_ativo=aging,intervalo_recalculo=int(intervalo),
                    cota_ativa=cota,cota_n=int(cota_n),
                    sla={Categoria.NIVEL_4:int(n4),Categoria.NIVEL_3:int(n3),Categoria.NIVEL_2:int(n2),Categoria.NIVEL_1:int(n1)},
                    limite_starvation=int(limite))
                seed=int(semente) if semente.strip().isdigit() else None
                reiniciar(config,seed); st.session_state["semente_atual"]=seed
                st.session_state["automatico"]=False
                st.toast("Configurações aplicadas. Simulação reiniciada.")
                st.rerun()
            except Exception as erro:
                st.error(f"Não foi possível aplicar as configurações: {erro}")
        st.divider()
        if st.button("🔄 Reiniciar simulação",key="reiniciar"):
            seed=int(semente) if semente.strip().isdigit() else None
            reiniciar(cfg,seed); st.session_state["automatico"]=False
            st.toast("Simulação reiniciada."); st.rerun()
        st.caption("O tempo é simulado: ele avança somente pelas ações ou pelo modo automático.")

def _dados_kpis():
    s=st.session_state.servico; m=st.session_state.metricas
    atendidos=m.total_atendidos()
    ocupados=sum(not g.esta_livre() for g in s.guiches)
    maior,senha=m.maior_espera()
    return [
        {"titulo":"Aguardando","valor":s.tamanho_fila(),"detalhe":"pessoas na fila","tom":"risco" if s.tamanho_fila() else ""},
        {"titulo":"Em atendimento","valor":ocupados,"detalhe":f"de {len(s.guiches)} guichês"},
        {"titulo":"Atendidos","valor":atendidos,"detalhe":"total da simulação","tom":"ok"},
        {"titulo":"Dentro do SLA","valor":f'{m.percentual_dentro_sla():.1f}%',"detalhe":"dos atendimentos concluídos","tom":"ok" if m.percentual_dentro_sla()>=90 else "risco"},
        {"titulo":"Maior espera","valor":f"{maior} min","detalhe":f"senha {senha}"}
    ]

def _linha_kpis():
    _html(comp.kpis(_dados_kpis()))

def pagina_painel():
    s=st.session_state.servico
    st.subheader("📊 Visão geral")
    _linha_kpis()
    st.markdown(comp.aviso(f'🕒 Horário simulado: <b>{s.relogio.agora().strftime("%d/%m/%Y %H:%M")}</b> · O relógio avança conforme os comandos de simulação.'),unsafe_allow_html=True)
    st.markdown("#### 🎛️ Central de operações")
    a,b,c,d=st.columns([1.2,1.2,1.2,1.2])
    tipos=catalogo_padrao()
    with a:
        categoria=st.selectbox("Categoria",list(Categoria),format_func=lambda x:x.nome_curto,key="manual_categoria")
        tipo=st.selectbox("Serviço",tipos,format_func=lambda x:f"{x.nome} · {x.minutos} min",key="manual_tipo")
        if st.button("➕ Adicionar pessoa",type="primary",key="adicionar_manual"):
            s.gerar_cliente(categoria,tipo); st.toast("Pessoa adicionada à fila.")
            st.rerun()
    with b:
        qtd=st.number_input("Quantidade aleatória",1,500,5,key="qtd_aleatorios")
        st.caption("Distribuição: 1% N4 · 12% N3 · 10% N2 · 77% N1")
        if st.button("🎲 Gerar pessoas",key="gerar_aleatorios"):
            for _ in range(int(qtd)):
                cat,idade,tp=st.session_state.gerador.sortear_cliente()
                s._entrar_na_fila(cat,tp,idade)
            s._chamar_proximos(); st.toast(f"{qtd} pessoas geradas."); st.rerun()
    with c:
        minutos=st.number_input("Avançar (minutos)",1,240,5,key="minutos_avanco")
        chegadas=st.checkbox("Simular novas chegadas",True,key="com_chegadas")
        if st.button("⏩ Avançar tempo",key="avancar"):
            s.avancar_tempo(int(minutos),st.session_state.gerador if chegadas else None)
            st.toast(f"Relógio avançado em {minutos} minutos."); st.rerun()
    with d:
        qtd_est=st.number_input("Pessoas no teste",10,1000,200,key="qtd_estresse")
        st.caption("Processa chegadas até concluir a fila.")
        if st.button("🧪 Executar estresse",key="estresse"):
            s.rodar_estresse(int(qtd_est),st.session_state.gerador)
            st.toast("Teste de estresse concluído."); st.rerun()
    st.divider()
    st.markdown("#### 🪟 Situação dos guichês")
    cols=st.columns(len(s.guiches))
    for col,g in zip(cols,s.guiches):
        with col:
            _html(comp.guiche(g.numero,g.cliente_atual,max(0,g.minuto_fim-s.relogio.minuto_atual),g.total_atendidos))
    st.markdown("#### 🏁 Próximas pessoas")
    fila=s.fila_ordenada()
    if fila:
        for i,cliente in enumerate(fila[:int(st.session_state.get("cfg_limite_cartoes",8))],1):
            _html(comp.cartao_cliente(cliente,i,cliente.espera(s.relogio.minuto_atual),s.config.sla[cliente.categoria],i==1))
        if len(fila)>int(st.session_state.get("cfg_limite_cartoes",8)):
            st.caption(f"… e mais {len(fila)-int(st.session_state.get('cfg_limite_cartoes',8))} pessoa(s). Consulte a página Filas.")
    else:
        _html(comp.vazio("A fila está vazia. Adicione pessoas ou gere uma entrada aleatória."))

def pagina_filas():
    s=st.session_state.servico; agora=s.relogio.minuto_atual
    st.subheader("📋 Acompanhamento das filas")
    _linha_kpis()
    chegada=s.fila_por_chegada(); prioridade=s.fila_ordenada()
    col1,col2=st.columns(2,gap="large")
    limite=int(st.session_state.get("cfg_limite_cartoes",8))
    with col1:
        st.markdown("#### ① Ordem de chegada")
        st.caption("Sequência cronológica em que as pessoas entraram.")
        if chegada:
            for i,c in enumerate(chegada[:limite],1):
                _html(comp.cartao_cliente(c,i,c.espera(agora),s.config.sla[c.categoria]))
            if len(chegada)>limite: st.caption(f"… e mais {len(chegada)-limite} pessoa(s).")
        else: _html(comp.vazio("Não há pessoas aguardando."))
        with st.expander("📋 Ver tabela completa — chegada"):
            dados=[{"Ordem":i,"Senha":c.senha,"Categoria":c.categoria.nome_curto,"Idade":c.idade,
                    "Serviço":c.tipo_servico.nome,"Espera (min)":c.espera(agora),"SLA (min)":s.config.sla[c.categoria]}
                   for i,c in enumerate(chegada,1)]
            st.dataframe(pd.DataFrame(dados),hide_index=True,width="stretch") if dados else st.caption("Sem registros.")
    with col2:
        st.markdown("#### ② Ordem de atendimento")
        st.caption("Ordenação calculada pelo heap, considerando prioridade e aging.")
        if prioridade:
            for i,c in enumerate(prioridade[:limite],1):
                _html(comp.cartao_cliente(c,i,c.espera(agora),s.config.sla[c.categoria],i==1))
            if len(prioridade)>limite: st.caption(f"… e mais {len(prioridade)-limite} pessoa(s).")
        else: _html(comp.vazio("Não há pessoas aguardando."))
        with st.expander("📋 Ver tabela completa — prioridade"):
            dados=[{"Posição":i,"Senha":c.senha,"Categoria":c.categoria.nome_curto,"Pontuação":("Prioridade absoluta" if c.categoria==Categoria.NIVEL_4 else round(c.pontuacao_atual,2)),
                    "Espera (min)":c.espera(agora),"SLA (min)":s.config.sla[c.categoria]}
                   for i,c in enumerate(prioridade,1)]
            st.dataframe(pd.DataFrame(dados),hide_index=True,width="stretch") if dados else st.caption("Sem registros.")

def pagina_guiches():
    s=st.session_state.servico
    st.subheader("🪟 Guichês de atendimento")
    _linha_kpis()
    cols=st.columns(min(3,len(s.guiches)))
    for i,g in enumerate(s.guiches):
        with cols[i%len(cols)]:
            _html(comp.guiche(g.numero,g.cliente_atual,max(0,g.minuto_fim-s.relogio.minuto_atual),g.total_atendidos))
    livres=sum(g.esta_livre() for g in s.guiches)
    _html(comp.aviso(f'{livres} guichê(s) livre(s) · {len(s.guiches)-livres} ocupado(s).', "verde" if livres else ""))

def _linhas_atendimentos(atendimentos,s):
    linhas=[]
    for ordem,a in enumerate(reversed(atendimentos),1):
        linhas.append({"Ordem":len(atendimentos)-ordem+1,"Senha":("👑" if a.cliente.categoria==Categoria.NIVEL_4 else "")+a.cliente.senha,
            "Categoria":a.cliente.categoria.nome_curto,"Idade":f"{a.cliente.idade} anos","Serviço":a.cliente.tipo_servico.nome,
            "Chegada":s.relogio.para_datetime(a.cliente.minuto_chegada).strftime("%H:%M"),
            "Chamado":s.relogio.para_datetime(a.minuto_inicio).strftime("%H:%M"),
            "Espera":f"{a.tempo_espera} min","Atendimento":f"{a.minuto_fim-a.minuto_inicio} min",
            "Guichê":a.id_guiche,"SLA":f"{a.sla_minutos} min","Status":a.status_sla,"Motivo":a.motivo})
    return linhas

def pagina_atendimentos():
    s=st.session_state.servico; m=st.session_state.metricas
    st.subheader("🧾 Atendimentos e histórico")
    _linha_kpis()
    atendimentos=s.repo_atendimentos.listar()
    if atendimentos:
        dados=_linhas_atendimentos(atendimentos,s)
        st.dataframe(pd.DataFrame(dados),hide_index=True,width="stretch",height=430)
    else: _html(comp.vazio("Ainda não houve atendimentos. As chamadas aparecerão aqui."))

def pagina_indicadores():
    s=st.session_state.servico; m=st.session_state.metricas
    st.subheader("📈 Indicadores e auditoria")
    _linha_kpis()
    maior,senha=m.maior_espera()
    medias=m.tempo_medio_por_categoria()
    tabela=pd.DataFrame([{"Categoria":c.nome_curto,"Tempo médio de espera (min)":round(medias[c],1),
        "Dentro do SLA (%)":round(m.percentual_dentro_sla(c),1),"SLA configurado (min)":s.config.sla[c]} for c in Categoria])
    st.markdown("#### Desempenho por categoria")
    st.dataframe(tabela,hide_index=True,width="stretch")
    c1,c2=st.columns(2)
    with c1: st.metric("Alertas de starvation",m.starvation_detectados())
    with c2: st.metric("Casos de starvation evitados",m.starvation_evitado())
    eventos=[e for e in s.repo_eventos.listar() if e.tipo in (TipoEvento.ALERTA_SLA,TipoEvento.STARVATION)]
    st.markdown("#### ⚠️ Alertas de SLA e espera excessiva")
    if eventos:
        dados=[{"Horário":s.relogio.para_datetime(e.minuto).strftime("%H:%M"),"Tipo":e.tipo.value,
            "Senha":e.cliente.senha,"Categoria":e.cliente.categoria.nome_curto,
            "Espera":f"{e.tempo_espera} min","Detalhe":e.observacao} for e in reversed(eventos)]
        st.dataframe(pd.DataFrame(dados),hide_index=True,width="stretch")
    else: _html(comp.aviso("Nenhum alerta de SLA ou starvation foi registrado.", "verde"))
    st.markdown("#### 💾 Exportação de auditoria SQL")
    texto=st.session_state.gerador_sql.gerar(s.guiches,s.repo_eventos.listar(),s.repo_atendimentos.listar())
    st.download_button("⬇️ Baixar arquivo logsA3.sql",texto,file_name="logsA3.sql",mime="text/plain",
        help="Exporta os eventos e atendimentos registrados nesta simulação.")

def pagina_placeholder():
    pass
