from dominio.categoria import Categoria
from dominio.evento_fila import TipoEvento


class Metricas:
    def __init__(self, repo_atendimentos, repo_eventos):
        self.repo_atendimentos = repo_atendimentos
        self.repo_eventos = repo_eventos

    def tempo_medio_por_categoria(self):
        medias = {}
        for categoria in Categoria:
            lista = self.repo_atendimentos.listar_por_categoria(categoria)
            if lista:
                medias[categoria] = sum(a.tempo_espera for a in lista) / len(lista)
            else:
                medias[categoria] = 0.0
        return medias

    def percentual_dentro_sla(self, categoria=None):
        if categoria is None:
            lista = self.repo_atendimentos.listar()
        else:
            lista = self.repo_atendimentos.listar_por_categoria(categoria)
        if not lista:
            return 0.0
        dentro = sum(1 for a in lista if a.dentro_sla)
        return 100.0 * dentro / len(lista)

    def maior_espera(self):
        lista = self.repo_atendimentos.listar()
        if not lista:
            return 0, "-"
        pior = max(lista, key=lambda a: a.tempo_espera)
        return pior.tempo_espera, pior.cliente.senha

    def starvation_detectados(self):
        return len(self.repo_eventos.listar_por_tipo(TipoEvento.STARVATION))

    def starvation_evitado(self):
        # detectado e depois atendido porque o aging ou a cota entrou em ação
        return sum(1 for a in self.repo_atendimentos.listar()
                   if a.cliente.starvation_detectado and a.motivo != "NORMAL")

    def total_atendidos(self):
        return len(self.repo_atendimentos.listar())
