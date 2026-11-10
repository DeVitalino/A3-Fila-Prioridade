from dominio.categoria import Categoria
from testes.auxiliar import FINANCIAMENTO, SAQUE, montar_servico


def montar_fila_com_prioritarios(servico, quantidade):
    servico.gerar_cliente(Categoria.VIP, FINANCIAMENTO)  # segura o guichê
    comum = servico.gerar_cliente(Categoria.COMUM, SAQUE)
    for _ in range(quantidade):
        servico.gerar_cliente(Categoria.PRIORITARIO, SAQUE)
    return comum


def senhas_atendidas(servico):
    return [a.cliente.senha for a in servico.repo_atendimentos.listar()]


def test_cota_chama_comum_depois_de_n_prioritarios():
    servico = montar_servico(qtd_guiches=1, cota_n=2, aging_ativo=False)
    comum = montar_fila_com_prioritarios(servico, 5)
    servico.avancar_tempo(25 + 3 * 3)
    ordem = senhas_atendidas(servico)
    # V001, depois dois prioritários, depois o comum pela cota
    assert ordem[1:3] == ["P001", "P002"]
    assert ordem[3] == comum.senha
    assert servico.repo_atendimentos.listar()[3].motivo == "COTA"


def test_sem_cota_o_comum_espera_todos_os_prioritarios():
    servico = montar_servico(qtd_guiches=1, cota_ativa=False, aging_ativo=False)
    comum = montar_fila_com_prioritarios(servico, 5)
    servico.avancar_tempo(25 + 3 * 5)
    assert senhas_atendidas(servico).index(comum.senha) == 6


def test_cota_ignorada_quando_nao_tem_comum_esperando():
    servico = montar_servico(qtd_guiches=1, cota_n=1, aging_ativo=False)
    servico.gerar_cliente(Categoria.VIP, FINANCIAMENTO)
    for _ in range(3):
        servico.gerar_cliente(Categoria.PRIORITARIO, SAQUE)
    servico.avancar_tempo(25 + 3 * 3)
    assert len(servico.repo_atendimentos.listar()) == 4
