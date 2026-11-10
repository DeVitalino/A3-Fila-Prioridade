from dominio.configuracao import Configuracao
from dominio.tipo_servico import TipoServico
from repositorio.repositorio_atendimentos import RepositorioAtendimentos
from repositorio.repositorio_clientes import RepositorioClientes
from repositorio.repositorio_eventos import RepositorioEventos
from servico.relogio_simulado import RelogioSimulado
from servico.servico_fila import ServicoFila

SAQUE = TipoServico("Saque", 3)
FINANCIAMENTO = TipoServico("Financiamento", 25)


def montar_servico(**opcoes):
    config = Configuracao(**opcoes)
    relogio = RelogioSimulado(config.data_base)
    return ServicoFila(config, relogio, RepositorioClientes(),
                       RepositorioEventos(), RepositorioAtendimentos())
