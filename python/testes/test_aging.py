from dominio.categoria import Categoria
from testes.auxiliar import FINANCIAMENTO, SAQUE, montar_servico


def ocupar_guiche(servico):
    # um atendimento longo segura o único guichê enquanto a fila envelhece
    servico.gerar_cliente(Categoria.VIP, FINANCIAMENTO)


def test_aging_sobe_a_prioridade_de_quem_espera():
    servico = montar_servico(qtd_guiches=1, minutos_por_nivel=10, intervalo_recalculo=5)
    ocupar_guiche(servico)
    comum = servico.gerar_cliente(Categoria.COMUM, SAQUE)
    servico.avancar_tempo(20)
    assert comum.prioridade_efetiva == 0


def test_comum_antigo_passa_na_frente_de_prioritario_novo():
    servico = montar_servico(qtd_guiches=1, minutos_por_nivel=10, intervalo_recalculo=5)
    ocupar_guiche(servico)
    comum = servico.gerar_cliente(Categoria.COMUM, SAQUE)
    servico.avancar_tempo(20)
    prioritario = servico.gerar_cliente(Categoria.PRIORITARIO, SAQUE)
    servico._aplicar_aging()
    assert servico.fila_ordenada() == [comum, prioritario]


def test_sem_aging_a_prioridade_nao_muda():
    servico = montar_servico(qtd_guiches=1, aging_ativo=False)
    ocupar_guiche(servico)
    comum = servico.gerar_cliente(Categoria.COMUM, SAQUE)
    servico.avancar_tempo(20)
    assert comum.prioridade_efetiva == Categoria.COMUM.prioridade_base


def test_atendimento_por_aging_fica_registrado():
    servico = montar_servico(qtd_guiches=1, minutos_por_nivel=10, intervalo_recalculo=5)
    ocupar_guiche(servico)
    servico.gerar_cliente(Categoria.COMUM, SAQUE)
    servico.avancar_tempo(25)  # o financiamento termina no minuto 25
    ultimo = servico.repo_atendimentos.listar()[-1]
    assert ultimo.cliente.categoria == Categoria.COMUM
    assert ultimo.motivo == "AGING"
