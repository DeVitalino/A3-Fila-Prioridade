"""
Testes de SLA (atualizados para 4 níveis).
"""
from dominio.categoria import Categoria
from dominio.evento_fila import TipoEvento
from servico.metricas import Metricas
from testes.auxiliar import FINANCIAMENTO, SAQUE, montar_servico


def test_atendimento_dentro_do_sla():
    servico = montar_servico(qtd_guiches=1)
    servico.gerar_cliente(Categoria.NIVEL_1, SAQUE, idade=30)
    atendimento = servico.repo_atendimentos.listar()[0]
    assert atendimento.tempo_espera == 0
    assert atendimento.dentro_sla


def test_atendimento_fora_do_sla():
    servico = montar_servico(qtd_guiches=1, aging_ativo=False)
    servico.gerar_cliente(Categoria.NIVEL_3, FINANCIAMENTO, idade=65)
    servico.gerar_cliente(Categoria.NIVEL_3, SAQUE, idade=70)
    servico.avancar_tempo(25)
    segundo = servico.repo_atendimentos.listar()[1]
    assert segundo.tempo_espera == 25
    assert segundo.status_sla == "FORA"


def test_alerta_quando_perto_de_estourar():
    servico = montar_servico(qtd_guiches=1, aging_ativo=False)
    servico.gerar_cliente(Categoria.NIVEL_3, FINANCIAMENTO, idade=65)
    n3 = servico.gerar_cliente(Categoria.NIVEL_3, SAQUE, idade=70)
    servico.avancar_tempo(11)
    assert not n3.alerta_sla_emitido
    servico.avancar_tempo(1)  # 12 min = 80% de 15
    assert n3.alerta_sla_emitido
    assert servico.situacao_sla(n3) == "Perto do SLA"
    alertas = servico.repo_eventos.listar_por_tipo(TipoEvento.ALERTA_SLA)
    assert len(alertas) == 1


def test_alerta_emitido_uma_vez_so():
    servico = montar_servico(qtd_guiches=1, aging_ativo=False)
    servico.gerar_cliente(Categoria.NIVEL_3, FINANCIAMENTO, idade=65)
    servico.gerar_cliente(Categoria.NIVEL_3, SAQUE, idade=70)
    servico.avancar_tempo(20)
    assert len(servico.repo_eventos.listar_por_tipo(TipoEvento.ALERTA_SLA)) == 1


def test_starvation_detectado_e_resolvido_pelo_aging():
    servico = montar_servico(qtd_guiches=1, limite_starvation=20, aging_ativo=True, intervalo_recalculo=5)
    servico.gerar_cliente(Categoria.NIVEL_3, FINANCIAMENTO, idade=65)
    comum = servico.gerar_cliente(Categoria.NIVEL_1, SAQUE, idade=30)
    servico.avancar_tempo(30)
    assert comum.starvation_detectado
    metricas = Metricas(servico.repo_atendimentos, servico.repo_eventos)
    assert metricas.starvation_detectados() == 1
    assert metricas.starvation_evitado() == 1


def test_metricas_de_percentual_e_maior_espera():
    servico = montar_servico(qtd_guiches=1, aging_ativo=False)
    servico.gerar_cliente(Categoria.NIVEL_3, FINANCIAMENTO, idade=65)
    servico.gerar_cliente(Categoria.NIVEL_3, SAQUE, idade=70)
    servico.avancar_tempo(30)
    metricas = Metricas(servico.repo_atendimentos, servico.repo_eventos)
    assert metricas.percentual_dentro_sla() == 50.0
    assert metricas.maior_espera() == (25, "N3002")
