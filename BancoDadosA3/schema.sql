-- Esquema de auditoria da fila bancária - Sistema de 4 Níveis
-- MySQL 8+ compatível
-- Rode este arquivo uma vez e depois o logsA3.sql gerado pelo simulador.

CREATE DATABASE IF NOT EXISTS banco_dados_a3 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE banco_dados_a3;

DROP TABLE IF EXISTS atendimentos;
DROP TABLE IF EXISTS eventos_fila;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS guiches;

CREATE TABLE guiches (
    id_guiche INT NOT NULL,
    nome VARCHAR(30) NOT NULL,
    PRIMARY KEY (id_guiche)
) ENGINE=InnoDB;

-- Uma linha por senha emitida
CREATE TABLE clientes (
    id_cliente INT NOT NULL,
    senha VARCHAR(10) NOT NULL,
    categoria ENUM('NIVEL_4', 'NIVEL_3', 'NIVEL_2', 'NIVEL_1') NOT NULL,
    idade INT NOT NULL,
    tipo_servico VARCHAR(40) NOT NULL,
    minutos_servico INT NOT NULL,
    data_hora_chegada DATETIME NOT NULL,
    PRIMARY KEY (id_cliente),
    UNIQUE KEY uk_clientes_senha (senha),
    INDEX idx_categoria (categoria),
    INDEX idx_idade (idade)
) ENGINE=InnoDB;

-- Toda entrada, saída, alerta de SLA e starvation vira uma linha aqui
CREATE TABLE eventos_fila (
    id_evento INT NOT NULL,
    id_cliente INT NOT NULL,
    tipo_evento ENUM('ENTRADA', 'SAIDA', 'ALERTA_SLA', 'STARVATION') NOT NULL,
    data_hora DATETIME NOT NULL,
    senha VARCHAR(10) NOT NULL,
    categoria ENUM('NIVEL_4', 'NIVEL_3', 'NIVEL_2', 'NIVEL_1') NOT NULL,
    id_guiche INT NULL,
    tempo_espera_min INT NOT NULL DEFAULT 0,
    status_sla ENUM('DENTRO', 'FORA') NULL,
    observacao VARCHAR(120) NULL,
    PRIMARY KEY (id_evento),
    KEY idx_eventos_cliente (id_cliente),
    KEY idx_eventos_data (data_hora),
    KEY idx_eventos_tipo (tipo_evento),
    CONSTRAINT fk_eventos_cliente FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
    CONSTRAINT fk_eventos_guiche FOREIGN KEY (id_guiche) REFERENCES guiches (id_guiche)
) ENGINE=InnoDB;

-- Uma linha por cliente chamado a um guichê
CREATE TABLE atendimentos (
    id_atendimento INT NOT NULL,
    id_cliente INT NOT NULL,
    id_guiche INT NOT NULL,
    data_hora_inicio DATETIME NOT NULL,
    data_hora_fim DATETIME NOT NULL,
    tempo_espera_min INT NOT NULL,
    sla_minutos INT NOT NULL,
    status_sla ENUM('DENTRO', 'FORA') NOT NULL,
    motivo_chamada ENUM('NORMAL', 'AGING', 'COTA') NOT NULL,
    PRIMARY KEY (id_atendimento),
    UNIQUE KEY uk_atendimentos_cliente (id_cliente),
    KEY idx_status_sla (status_sla),
    KEY idx_motivo (motivo_chamada),
    CONSTRAINT fk_atendimentos_cliente FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
    CONSTRAINT fk_atendimentos_guiche FOREIGN KEY (id_guiche) REFERENCES guiches (id_guiche)
) ENGINE=InnoDB;

-- Comentários explicativos
ALTER TABLE clientes COMMENT = 'Registro de todos os clientes que entraram na fila';
ALTER TABLE eventos_fila COMMENT = 'Log de todos os eventos: entradas, saídas, alertas SLA e starvation';
ALTER TABLE atendimentos COMMENT = 'Histórico de atendimentos realizados nos guichês';
