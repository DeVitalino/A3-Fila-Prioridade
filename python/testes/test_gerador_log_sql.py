from dominio.categoria import Categoria
from repositorio.gerador_log_sql import GeradorLogSql
from testes.auxiliar import FINANCIAMENTO, SAQUE, montar_servico


def gerar_sql(servico):
    gerador = GeradorLogSql(servico.relogio)
    return gerador.gerar(servico.guiches, servico.repo_eventos.listar(),
                         servico.repo_atendimentos.listar())


def cenario_simples():
    servico = montar_servico(qtd_guiches=1)
    servico.gerar_cliente(Categoria.PRIORITARIO, SAQUE)
    servico.gerar_cliente(Categoria.COMUM, FINANCIAMENTO)
    servico.avancar_tempo(5)
    return servico


def test_toda_transacao_abre_e_fecha():
    sql = gerar_sql(cenario_simples())
    assert sql.count("START TRANSACTION;") == sql.count("COMMIT;")


def test_entrada_gera_insert_de_cliente_e_evento():
    sql = gerar_sql(cenario_simples())
    assert "INSERT INTO clientes" in sql
    assert "'ENTRADA'" in sql
    assert "'P001'" in sql


def test_saida_gera_evento_e_atendimento_com_sla():
    sql = gerar_sql(cenario_simples())
    assert "'SAIDA'" in sql
    assert "INSERT INTO atendimentos" in sql
    assert "'DENTRO'" in sql


def test_data_hora_vem_do_relogio_simulado():
    sql = gerar_sql(cenario_simples())
    assert "'2026-11-09 08:00:00'" in sql


def test_aspas_no_texto_sao_escapadas():
    gerador = GeradorLogSql(montar_servico().relogio)
    assert gerador._texto("O'Brien") == "'O''Brien'"


def test_salvar_cria_arquivo(tmp_path):
    servico = cenario_simples()
    caminho = tmp_path / "logs.sql"
    GeradorLogSql(servico.relogio).salvar(
        caminho, servico.guiches, servico.repo_eventos.listar(),
        servico.repo_atendimentos.listar())
    assert caminho.read_text(encoding="utf-8").startswith("-- logs.sql")
