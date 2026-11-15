"""
Testes para o sistema de 4 níveis de prioridade.
"""
from dominio.categoria import Categoria
from testes.auxiliar import SAQUE, montar_servico


def test_categoria_por_idade():
    """Testa classificação automática por idade."""
    assert Categoria.por_idade(85) == Categoria.NIVEL_4
    assert Categoria.por_idade(80) == Categoria.NIVEL_4
    assert Categoria.por_idade(79) == Categoria.NIVEL_3
    assert Categoria.por_idade(60) == Categoria.NIVEL_3
    assert Categoria.por_idade(59) == Categoria.NIVEL_1
    assert Categoria.por_idade(30, tem_deficiencia=True) == Categoria.NIVEL_2
    assert Categoria.por_idade(85, tem_deficiencia=True) == Categoria.NIVEL_4  # Idade prevalece


def test_nivel_4_sempre_primeiro():
    """NIVEL_4 (80+) deve sempre ter prioridade absoluta."""
    servico = montar_servico(qtd_guiches=1, aging_ativo=False)
    
    # Criar clientes de todos os níveis
    n1 = servico.gerar_cliente(Categoria.NIVEL_1, SAQUE, idade=30)
    n2 = servico.gerar_cliente(Categoria.NIVEL_2, SAQUE, idade=40)
    n3 = servico.gerar_cliente(Categoria.NIVEL_3, SAQUE, idade=65)
    n4 = servico.gerar_cliente(Categoria.NIVEL_4, SAQUE, idade=85)
    
    # O último a chegar (NIVEL_4) deve estar primeiro na fila
    fila = servico.fila_ordenada()
    assert fila[0] == n4
    assert fila[1] == n3
    assert fila[2] == n2
    assert fila[3] == n1


def test_nivel_4_nao_afetado_por_aging():
    """NIVEL_4 não deve ser afetado pelo aging."""
    servico = montar_servico(qtd_guiches=1, aging_ativo=True)
    
    n4 = servico.gerar_cliente(Categoria.NIVEL_4, SAQUE, idade=85)
    pontuacao_inicial = n4.pontuacao_atual
    
    # Avançar tempo significativo
    servico.avancar_tempo(100)
    
    # Pontuação não deve mudar
    assert n4.pontuacao_atual == pontuacao_inicial


def test_ordem_de_chegada_vs_calculada():
    """Testa que as duas listas são diferentes mas contêm os mesmos clientes."""
    servico = montar_servico(qtd_guiches=1, aging_ativo=False)
    
    # Criar em ordem: N1, N3, N2
    n1 = servico.gerar_cliente(Categoria.NIVEL_1, SAQUE, idade=30)
    n3 = servico.gerar_cliente(Categoria.NIVEL_3, SAQUE, idade=65)
    n2 = servico.gerar_cliente(Categoria.NIVEL_2, SAQUE, idade=40)
    
    chegada = servico.fila_por_chegada()
    calculada = servico.fila_ordenada()
    
    # Chegada: N1, N3, N2
    assert chegada == [n1, n3, n2]
    
    # Calculada: N3, N2, N1 (por prioridade)
    assert calculada == [n3, n2, n1]


def test_prioridade_efetiva_com_idade():
    """Testa que clientes são criados com idade correta."""
    servico = montar_servico(qtd_guiches=1)
    
    c1 = servico.gerar_cliente(Categoria.NIVEL_4, SAQUE, idade=85)
    c2 = servico.gerar_cliente(Categoria.NIVEL_3, SAQUE, idade=70)
    c3 = servico.gerar_cliente(Categoria.NIVEL_2, SAQUE, idade=35)
    c4 = servico.gerar_cliente(Categoria.NIVEL_1, SAQUE, idade=25)
    
    assert c1.idade == 85
    assert c2.idade == 70
    assert c3.idade == 35
    assert c4.idade == 25
