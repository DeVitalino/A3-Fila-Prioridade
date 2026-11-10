from dominio.evento_fila import TipoEvento


class GeradorLogSql:
    def __init__(self, relogio):
        self.relogio = relogio

    def gerar(self, guiches, eventos, atendimentos):
        por_cliente = {a.cliente.id_cliente: a for a in atendimentos}
        linhas = [
            "-- logs.sql gerado pelo simulador (versão Python)",
            "-- rode sql/schema.sql antes deste arquivo",
            "USE fila_banco;",
            "SET NAMES utf8mb4;",
            "",
        ]
        linhas += self._limpeza_e_guiches(guiches)
        for evento in eventos:
            if evento.tipo == TipoEvento.ENTRADA:
                linhas += self._entrada(evento)
            elif evento.tipo == TipoEvento.SAIDA:
                linhas += self._saida(evento, por_cliente[evento.cliente.id_cliente])
            else:
                linhas += self._outro_evento(evento)
        return "\n".join(linhas) + "\n"

    def salvar(self, caminho, guiches, eventos, atendimentos):
        texto = self.gerar(guiches, eventos, atendimentos)
        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)

    def _limpeza_e_guiches(self, guiches):
        # apaga na ordem inversa das chaves estrangeiras para poder rodar de novo
        linhas = [
            "START TRANSACTION;",
            "DELETE FROM atendimentos;",
            "DELETE FROM eventos_fila;",
            "DELETE FROM clientes;",
            "DELETE FROM guiches;",
        ]
        for g in guiches:
            linhas.append(
                f"INSERT INTO guiches (id_guiche, nome) VALUES ({g.numero}, {self._texto('Guichê ' + str(g.numero))});"
            )
        linhas += ["COMMIT;", ""]
        return linhas

    def _entrada(self, evento):
        c = evento.cliente
        return [
            "START TRANSACTION;",
            "INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) "
            f"VALUES ({c.id_cliente}, {self._texto(c.senha)}, {self._texto(c.categoria.name)}, "
            f"{self._texto(c.tipo_servico.nome)}, {c.tipo_servico.minutos}, {self._data(c.minuto_chegada)});",
            self._insert_evento(evento),
            "COMMIT;",
            "",
        ]

    def _saida(self, evento, atendimento):
        c = evento.cliente
        return [
            "START TRANSACTION;",
            self._insert_evento(evento),
            "INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, "
            "tempo_espera_min, sla_minutos, status_sla, motivo_chamada) "
            f"VALUES ({atendimento.id_atendimento}, {c.id_cliente}, {atendimento.id_guiche}, "
            f"{self._data(atendimento.minuto_inicio)}, {self._data(atendimento.minuto_fim)}, "
            f"{atendimento.tempo_espera}, {atendimento.sla_minutos}, {self._texto(atendimento.status_sla)}, "
            f"{self._texto(atendimento.motivo)});",
            "COMMIT;",
            "",
        ]

    def _outro_evento(self, evento):
        return ["START TRANSACTION;", self._insert_evento(evento), "COMMIT;", ""]

    def _insert_evento(self, evento):
        c = evento.cliente
        return (
            "INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, "
            "id_guiche, tempo_espera_min, status_sla, observacao) "
            f"VALUES ({evento.id_evento}, {c.id_cliente}, {self._texto(evento.tipo.value)}, "
            f"{self._data(evento.minuto)}, {self._texto(c.senha)}, {self._texto(c.categoria.name)}, "
            f"{self._numero(evento.id_guiche)}, {evento.tempo_espera}, {self._texto(evento.status_sla)}, "
            f"{self._texto(evento.observacao)});"
        )

    def _data(self, minuto):
        momento = self.relogio.para_datetime(minuto)
        return "'" + momento.strftime("%Y-%m-%d %H:%M:%S") + "'"

    def _texto(self, valor):
        if valor is None:
            return "NULL"
        limpo = str(valor).replace("\\", "\\\\").replace("'", "''")
        return "'" + limpo + "'"

    def _numero(self, valor):
        return "NULL" if valor is None else str(valor)
