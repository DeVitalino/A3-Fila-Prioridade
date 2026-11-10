-- Esquema de auditoria da fila de banco (MySQL 8)
-- Rode este arquivo uma vez e depois o logs.sql gerado pelo simulador.

CREATE DATABASE IF NOT EXISTS fila_banco CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE fila_banco;

DROP TABLE IF EXISTS atendimentos;
DROP TABLE IF EXISTS eventos_fila;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS guiches;

CREATE TABLE guiches (
    id_guiche INT NOT NULL,
    nome VARCHAR(30) NOT NULL,
    PRIMARY KEY (id_guiche)
) ENGINE=InnoDB;

-- uma linha por senha emitida
CREATE TABLE clientes (
    id_cliente INT NOT NULL,
    senha VARCHAR(10) NOT NULL,
    categoria ENUM('PRIORITARIO', 'VIP', 'COMUM') NOT NULL,
    tipo_servico VARCHAR(40) NOT NULL,
    minutos_servico INT NOT NULL,
    data_hora_chegada DATETIME NOT NULL,
    PRIMARY KEY (id_cliente),
    UNIQUE KEY uk_clientes_senha (senha)
) ENGINE=InnoDB;

-- toda entrada, saída, alerta de SLA e starvation vira uma linha aqui
CREATE TABLE eventos_fila (
    id_evento INT NOT NULL,
    id_cliente INT NOT NULL,
    tipo_evento ENUM('ENTRADA', 'SAIDA', 'ALERTA_SLA', 'STARVATION') NOT NULL,
    data_hora DATETIME NOT NULL,
    senha VARCHAR(10) NOT NULL,
    categoria ENUM('PRIORITARIO', 'VIP', 'COMUM') NOT NULL,
    id_guiche INT NULL,
    tempo_espera_min INT NOT NULL DEFAULT 0,
    status_sla ENUM('DENTRO', 'FORA') NULL,
    observacao VARCHAR(120) NULL,
    PRIMARY KEY (id_evento),
    KEY idx_eventos_cliente (id_cliente),
    KEY idx_eventos_data (data_hora),
    CONSTRAINT fk_eventos_cliente FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
    CONSTRAINT fk_eventos_guiche FOREIGN KEY (id_guiche) REFERENCES guiches (id_guiche)
) ENGINE=InnoDB;

-- uma linha por cliente chamado a um guichê
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
    CONSTRAINT fk_atendimentos_cliente FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
    CONSTRAINT fk_atendimentos_guiche FOREIGN KEY (id_guiche) REFERENCES guiches (id_guiche)
) ENGINE=InnoDB;
