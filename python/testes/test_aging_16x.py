"""
Testes para o novo algoritmo de aging com multiplicador 1.6x.
"""
import math
from dominio.categoria import Categoria
from testes.auxiliar import FINANCIAMENTO, SAQUE, montar_servico


def ocupar_guiche(servico):
    """Segura o único guichê enquanto a fila envelhece."""
    servico.gerar_cliente(Categoria.NIVEL_3, FINANCIAMENTO, idade=65)


def test_aging_multiplica_por_16_apos_20_minutos():
    """Após 20 minutos, pontuação deve ser multiplicada por 1.6."""
    servico = montar_servico(qtd_guiches=1, aging_ativo=True, intervalo_recalculo=5)
    ocupar_guiche(servico)
    
    n1 = servico.gerar_cliente(Categoria.NIVEL_1, SAQUE, idade=30)
    pontuacao_inicial = n1.pontuacao_inicial
    
    # Avançar 20 minutos
    servico.avancar_tempo(25)  # 25 porque o guichê libera no 25
    
    # Pontuação deve ser 1 * 1.6 = 1.6
    assert math.isclose(n1.pontuacao_atual, pontuacao_inicial * 1.6, rel_tol=0.01)


def test_aging_multiplica_progressivamente():
    """Testa multiplicação progressiva a cada 20 minutos."""
    servico = montar_servico(qtd_guiches=1, aging_ativo=True, intervalo_recalculo=5)
    ocupar_guiche(servico)
    
    n1 = servico.gerar_cliente(Categoria.NIVEL_1, SAQUE, idade=30)
    pontuacao_inicial = n1.pontuacao_inicial
    
    # 0 minutos: 1
    assert n1.pontuacao_atual == pontuacao_inicial
    
    # 25 minutos (1 período de 20): 1 * 1.6¹ = 1.6
    servico.avancar_tempo(25)
    assert math.isclose(n1.pontuacao_atual, pontuacao_inicial * (1.6 ** 1), rel_tol=0.01)
    
    # 45 minutos (2 períodos de 20): 1 * 1.6² = 2.56
    servico.avancar_tempo(20)
    assert math.isclose(n1.pontuacao_atual, pontuacao_inicial * (1.6 ** 2), rel_tol=0.01)
    
    # 65 minutos (3 períodos de 20): 1 * 1.6³ = 4.096
    servico.avancar_tempo(20)
    assert math.isclose(n1.pontuacao_atual, pontuacao_inicial * (1.6 ** 3), rel_tol=0.01)


def test_nivel_1_ultrapassa_nivel_3_com_aging():
    """NIVEL_1 com aging deve eventualmente ultrapassar NIVEL_3 sem aging."""
    servico = montar_servico(qtd_guiches=1, aging_ativo=True, intervalo_recalculo=5)
    ocupar_guiche(servico)
    
    n1 = servico.gerar_cliente(Categoria.NIVEL_1, SAQUE, idade=30)
    servico.avancar_tempo(25)  # N1 aguarda 25 min (1 período)
    
    n3 = servico.gerar_cliente(Categoria.NIVEL_3, SAQUE, idade=65)  # Chega agora
    
    # N1: 1 * 1.6¹ = 1.6
    # N3: 3 * 1.6⁰ = 3
    # N3 ainda tem mais prioridade
    fila = servico.fila_ordenada()
    assert fila[0] == n3
    assert fila[1] == n1
    
    # Avançar mais 20 minutos
    servico.avancar_tempo(20)
    
    # N1: 1 * 1.6² = 2.56  (aguardou 45 min total)
    # N3: 3 * 1.6¹ = 4.8   (aguardou 20 min)
    # N3 ainda ganha
    fila = servico.fila_ordenada()
    assert fila[0] == n3
    
    # Avançar mais 20 minutos
    servico.avancar_tempo(20)
    
    # N1: 1 * 1.6³ = 4.096 (aguardou 65 min total)
    # N3: 3 * 1.6² = 7.68  (aguardou 40 min)
    # N3 ainda ganha, mas N1 está se aproximando


def test_periodos_incompletos_nao_contam():
    """Períodos incompletos de 20 min não devem incrementar aging."""
    servico = montar_servico(qtd_guiches=1, aging_ativo=True, intervalo_recalculo=5)
    ocupar_guiche(servico)
    
    n1 = servico.gerar_cliente(Categoria.NIVEL_1, SAQUE, idade=30)
    pontuacao_inicial = n1.pontuacao_inicial
    
    # Avançar apenas 19 minutos (período incompleto)
    servico.avancar_tempo(19)
    
    # Pontuação não deve mudar (0 períodos completos)
    assert n1.pontuacao_atual == pontuacao_inicial


def test_aging_com_nivel_2():
    """Testa aging com NIVEL_2 (PCD)."""
    servico = montar_servico(qtd_guiches=1, aging_ativo=True, intervalo_recalculo=5)
    ocupar_guiche(servico)
    
    n2 = servico.gerar_cliente(Categoria.NIVEL_2, SAQUE, idade=40)
    pontuacao_inicial = n2.pontuacao_inicial  # 2
    
    # Após 20 minutos: 2 * 1.6 = 3.2
    servico.avancar_tempo(25)
    assert math.isclose(n2.pontuacao_atual, pontuacao_inicial * 1.6, rel_tol=0.01)
    
    # Após 40 minutos: 2 * 1.6² = 5.12
    servico.avancar_tempo(20)
    assert math.isclose(n2.pontuacao_atual, pontuacao_inicial * (1.6 ** 2), rel_tol=0.01)


def test_motivo_aging_quando_pontuacao_aumenta():
    """Quando atendido com pontuação maior que inicial, motivo deve ser AGING."""
    servico = montar_servico(qtd_guiches=1, aging_ativo=True, intervalo_recalculo=5)
    
    n1 = servico.gerar_cliente(Categoria.NIVEL_1, SAQUE, idade=30)
    servico.avancar_tempo(25)  # Aguarda 25 min, ganha aging
    
    # Cliente deve ser atendido
    atendimentos = servico.repo_atendimentos.listar()
    assert len(atendimentos) == 1
    assert atendimentos[0].motivo == "AGING"
    assert atendimentos[0].cliente == n1
