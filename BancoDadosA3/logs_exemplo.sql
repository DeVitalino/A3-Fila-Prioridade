-- logs.sql gerado pelo simulador (versão Python)
-- rode sql/schema.sql antes deste arquivo
USE fila_banco;
SET NAMES utf8mb4;

START TRANSACTION;
DELETE FROM atendimentos;
DELETE FROM eventos_fila;
DELETE FROM clientes;
DELETE FROM guiches;
INSERT INTO guiches (id_guiche, nome) VALUES (1, 'Guichê 1');
INSERT INTO guiches (id_guiche, nome) VALUES (2, 'Guichê 2');
INSERT INTO guiches (id_guiche, nome) VALUES (3, 'Guichê 3');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (1, 'V001', 'VIP', 'Depósito', 4, '2026-11-09 08:01:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (1, 1, 'ENTRADA', '2026-11-09 08:01:00', 'V001', 'VIP', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (2, 1, 'SAIDA', '2026-11-09 08:01:00', 'V001', 'VIP', 1, 0, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (1, 1, 1, '2026-11-09 08:01:00', '2026-11-09 08:05:00', 0, 10, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (2, 'P001', 'PRIORITARIO', 'Financiamento', 25, '2026-11-09 08:02:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (3, 2, 'ENTRADA', '2026-11-09 08:02:00', 'P001', 'PRIORITARIO', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (4, 2, 'SAIDA', '2026-11-09 08:02:00', 'P001', 'PRIORITARIO', 2, 0, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (2, 2, 2, '2026-11-09 08:02:00', '2026-11-09 08:27:00', 0, 15, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (3, 'C001', 'COMUM', 'Saque', 3, '2026-11-09 08:03:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (5, 3, 'ENTRADA', '2026-11-09 08:03:00', 'C001', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (4, 'V002', 'VIP', 'Abertura de conta', 15, '2026-11-09 08:03:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (6, 4, 'ENTRADA', '2026-11-09 08:03:00', 'V002', 'VIP', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (7, 4, 'SAIDA', '2026-11-09 08:03:00', 'V002', 'VIP', 3, 0, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (3, 4, 3, '2026-11-09 08:03:00', '2026-11-09 08:18:00', 0, 10, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (5, 'P002', 'PRIORITARIO', 'Financiamento', 25, '2026-11-09 08:04:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (8, 5, 'ENTRADA', '2026-11-09 08:04:00', 'P002', 'PRIORITARIO', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (9, 5, 'SAIDA', '2026-11-09 08:05:00', 'P002', 'PRIORITARIO', 1, 1, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (4, 5, 1, '2026-11-09 08:05:00', '2026-11-09 08:30:00', 1, 15, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (6, 'V003', 'VIP', 'Pagamento de boleto', 5, '2026-11-09 08:10:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (10, 6, 'ENTRADA', '2026-11-09 08:10:00', 'V003', 'VIP', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (7, 'V004', 'VIP', 'Pagamento de boleto', 5, '2026-11-09 08:17:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (11, 7, 'ENTRADA', '2026-11-09 08:17:00', 'V004', 'VIP', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (12, 6, 'ALERTA_SLA', '2026-11-09 08:18:00', 'V003', 'VIP', NULL, 8, NULL, 'perto de estourar o SLA de 10 min');
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (13, 3, 'SAIDA', '2026-11-09 08:18:00', 'C001', 'COMUM', 3, 15, 'DENTRO', 'chamada por AGING');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (5, 3, 3, '2026-11-09 08:18:00', '2026-11-09 08:21:00', 15, 30, 'DENTRO', 'AGING');
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (14, 6, 'SAIDA', '2026-11-09 08:21:00', 'V003', 'VIP', 3, 11, 'FORA', 'chamada por AGING');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (6, 6, 3, '2026-11-09 08:21:00', '2026-11-09 08:26:00', 11, 10, 'FORA', 'AGING');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (8, 'C002', 'COMUM', 'Abertura de conta', 15, '2026-11-09 08:23:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (15, 8, 'ENTRADA', '2026-11-09 08:23:00', 'C002', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (16, 7, 'ALERTA_SLA', '2026-11-09 08:25:00', 'V004', 'VIP', NULL, 8, NULL, 'perto de estourar o SLA de 10 min');
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (17, 7, 'SAIDA', '2026-11-09 08:26:00', 'V004', 'VIP', 3, 9, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (7, 7, 3, '2026-11-09 08:26:00', '2026-11-09 08:31:00', 9, 10, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (18, 8, 'SAIDA', '2026-11-09 08:27:00', 'C002', 'COMUM', 2, 4, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (8, 8, 2, '2026-11-09 08:27:00', '2026-11-09 08:42:00', 4, 30, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (9, 'V005', 'VIP', 'Pagamento de boleto', 5, '2026-11-09 08:28:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (19, 9, 'ENTRADA', '2026-11-09 08:28:00', 'V005', 'VIP', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (10, 'C003', 'COMUM', 'Abertura de conta', 15, '2026-11-09 08:29:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (20, 10, 'ENTRADA', '2026-11-09 08:29:00', 'C003', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (21, 9, 'SAIDA', '2026-11-09 08:30:00', 'V005', 'VIP', 1, 2, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (9, 9, 1, '2026-11-09 08:30:00', '2026-11-09 08:35:00', 2, 10, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (22, 10, 'SAIDA', '2026-11-09 08:31:00', 'C003', 'COMUM', 3, 2, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (10, 10, 3, '2026-11-09 08:31:00', '2026-11-09 08:46:00', 2, 30, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (11, 'P003', 'PRIORITARIO', 'Saque', 3, '2026-11-09 08:37:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (23, 11, 'ENTRADA', '2026-11-09 08:37:00', 'P003', 'PRIORITARIO', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (24, 11, 'SAIDA', '2026-11-09 08:37:00', 'P003', 'PRIORITARIO', 1, 0, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (11, 11, 1, '2026-11-09 08:37:00', '2026-11-09 08:40:00', 0, 15, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (12, 'C004', 'COMUM', 'Pagamento de boleto', 5, '2026-11-09 08:43:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (25, 12, 'ENTRADA', '2026-11-09 08:43:00', 'C004', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (26, 12, 'SAIDA', '2026-11-09 08:43:00', 'C004', 'COMUM', 1, 0, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (12, 12, 1, '2026-11-09 08:43:00', '2026-11-09 08:48:00', 0, 30, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (13, 'C005', 'COMUM', 'Financiamento', 25, '2026-11-09 08:46:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (27, 13, 'ENTRADA', '2026-11-09 08:46:00', 'C005', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (28, 13, 'SAIDA', '2026-11-09 08:46:00', 'C005', 'COMUM', 2, 0, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (13, 13, 2, '2026-11-09 08:46:00', '2026-11-09 09:11:00', 0, 30, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (14, 'V006', 'VIP', 'Saque', 3, '2026-11-09 08:53:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (29, 14, 'ENTRADA', '2026-11-09 08:53:00', 'V006', 'VIP', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (15, 'V007', 'VIP', 'Pagamento de boleto', 5, '2026-11-09 08:53:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (30, 15, 'ENTRADA', '2026-11-09 08:53:00', 'V007', 'VIP', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (31, 14, 'SAIDA', '2026-11-09 08:53:00', 'V006', 'VIP', 1, 0, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (14, 14, 1, '2026-11-09 08:53:00', '2026-11-09 08:56:00', 0, 10, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (32, 15, 'SAIDA', '2026-11-09 08:53:00', 'V007', 'VIP', 3, 0, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (15, 15, 3, '2026-11-09 08:53:00', '2026-11-09 08:58:00', 0, 10, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (16, 'C006', 'COMUM', 'Saque', 3, '2026-11-09 08:55:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (33, 16, 'ENTRADA', '2026-11-09 08:55:00', 'C006', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (34, 16, 'SAIDA', '2026-11-09 08:56:00', 'C006', 'COMUM', 1, 1, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (16, 16, 1, '2026-11-09 08:56:00', '2026-11-09 08:59:00', 1, 30, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (17, 'C007', 'COMUM', 'Abertura de conta', 15, '2026-11-09 08:57:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (35, 17, 'ENTRADA', '2026-11-09 08:57:00', 'C007', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (36, 17, 'SAIDA', '2026-11-09 08:58:00', 'C007', 'COMUM', 3, 1, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (17, 17, 3, '2026-11-09 08:58:00', '2026-11-09 09:13:00', 1, 30, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (18, 'P004', 'PRIORITARIO', 'Abertura de conta', 15, '2026-11-09 09:04:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (37, 18, 'ENTRADA', '2026-11-09 09:04:00', 'P004', 'PRIORITARIO', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (38, 18, 'SAIDA', '2026-11-09 09:04:00', 'P004', 'PRIORITARIO', 1, 0, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (18, 18, 1, '2026-11-09 09:04:00', '2026-11-09 09:19:00', 0, 15, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (19, 'C008', 'COMUM', 'Depósito', 4, '2026-11-09 09:06:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (39, 19, 'ENTRADA', '2026-11-09 09:06:00', 'C008', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (20, 'P005', 'PRIORITARIO', 'Pagamento de boleto', 5, '2026-11-09 09:06:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (40, 20, 'ENTRADA', '2026-11-09 09:06:00', 'P005', 'PRIORITARIO', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (21, 'V008', 'VIP', 'Financiamento', 25, '2026-11-09 09:07:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (41, 21, 'ENTRADA', '2026-11-09 09:07:00', 'V008', 'VIP', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (22, 'C009', 'COMUM', 'Pagamento de boleto', 5, '2026-11-09 09:11:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (42, 22, 'ENTRADA', '2026-11-09 09:11:00', 'C009', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (43, 20, 'SAIDA', '2026-11-09 09:11:00', 'P005', 'PRIORITARIO', 2, 5, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (19, 20, 2, '2026-11-09 09:11:00', '2026-11-09 09:16:00', 5, 15, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (44, 21, 'SAIDA', '2026-11-09 09:13:00', 'V008', 'VIP', 3, 6, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (20, 21, 3, '2026-11-09 09:13:00', '2026-11-09 09:38:00', 6, 10, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (23, 'C010', 'COMUM', 'Pagamento de boleto', 5, '2026-11-09 09:14:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (45, 23, 'ENTRADA', '2026-11-09 09:14:00', 'C010', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (24, 'P006', 'PRIORITARIO', 'Abertura de conta', 15, '2026-11-09 09:15:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (46, 24, 'ENTRADA', '2026-11-09 09:15:00', 'P006', 'PRIORITARIO', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (47, 24, 'SAIDA', '2026-11-09 09:16:00', 'P006', 'PRIORITARIO', 2, 1, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (21, 24, 2, '2026-11-09 09:16:00', '2026-11-09 09:31:00', 1, 15, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (48, 19, 'SAIDA', '2026-11-09 09:19:00', 'C008', 'COMUM', 1, 13, 'DENTRO', 'chamada por COTA');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (22, 19, 1, '2026-11-09 09:19:00', '2026-11-09 09:23:00', 13, 30, 'DENTRO', 'COTA');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (25, 'C011', 'COMUM', 'Saque', 3, '2026-11-09 09:20:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (49, 25, 'ENTRADA', '2026-11-09 09:20:00', 'C011', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (50, 22, 'SAIDA', '2026-11-09 09:23:00', 'C009', 'COMUM', 1, 12, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (23, 22, 1, '2026-11-09 09:23:00', '2026-11-09 09:28:00', 12, 30, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (26, 'V009', 'VIP', 'Atendimento de cartão', 8, '2026-11-09 09:24:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (51, 26, 'ENTRADA', '2026-11-09 09:24:00', 'V009', 'VIP', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (52, 23, 'SAIDA', '2026-11-09 09:28:00', 'C010', 'COMUM', 1, 14, 'DENTRO', 'chamada por AGING');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (24, 23, 1, '2026-11-09 09:28:00', '2026-11-09 09:33:00', 14, 30, 'DENTRO', 'AGING');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (27, 'C012', 'COMUM', 'Abertura de conta', 15, '2026-11-09 09:31:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (53, 27, 'ENTRADA', '2026-11-09 09:31:00', 'C012', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (54, 25, 'SAIDA', '2026-11-09 09:31:00', 'C011', 'COMUM', 2, 11, 'DENTRO', 'chamada por AGING');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (25, 25, 2, '2026-11-09 09:31:00', '2026-11-09 09:34:00', 11, 30, 'DENTRO', 'AGING');
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (55, 26, 'ALERTA_SLA', '2026-11-09 09:32:00', 'V009', 'VIP', NULL, 8, NULL, 'perto de estourar o SLA de 10 min');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (28, 'C013', 'COMUM', 'Depósito', 4, '2026-11-09 09:33:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (56, 28, 'ENTRADA', '2026-11-09 09:33:00', 'C013', 'COMUM', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (29, 'P007', 'PRIORITARIO', 'Depósito', 4, '2026-11-09 09:33:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (57, 29, 'ENTRADA', '2026-11-09 09:33:00', 'P007', 'PRIORITARIO', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (58, 29, 'SAIDA', '2026-11-09 09:33:00', 'P007', 'PRIORITARIO', 1, 0, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (26, 29, 1, '2026-11-09 09:33:00', '2026-11-09 09:37:00', 0, 15, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (59, 26, 'SAIDA', '2026-11-09 09:34:00', 'V009', 'VIP', 2, 10, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (27, 26, 2, '2026-11-09 09:34:00', '2026-11-09 09:42:00', 10, 10, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO clientes (id_cliente, senha, categoria, tipo_servico, minutos_servico, data_hora_chegada) VALUES (30, 'P008', 'PRIORITARIO', 'Financiamento', 25, '2026-11-09 09:36:00');
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (60, 30, 'ENTRADA', '2026-11-09 09:36:00', 'P008', 'PRIORITARIO', NULL, 0, NULL, NULL);
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (61, 30, 'SAIDA', '2026-11-09 09:37:00', 'P008', 'PRIORITARIO', 1, 1, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (28, 30, 1, '2026-11-09 09:37:00', '2026-11-09 10:02:00', 1, 15, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (62, 27, 'SAIDA', '2026-11-09 09:38:00', 'C012', 'COMUM', 3, 7, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (29, 27, 3, '2026-11-09 09:38:00', '2026-11-09 09:53:00', 7, 30, 'DENTRO', 'NORMAL');
COMMIT;

START TRANSACTION;
INSERT INTO eventos_fila (id_evento, id_cliente, tipo_evento, data_hora, senha, categoria, id_guiche, tempo_espera_min, status_sla, observacao) VALUES (63, 28, 'SAIDA', '2026-11-09 09:42:00', 'C013', 'COMUM', 2, 9, 'DENTRO', 'chamada por NORMAL');
INSERT INTO atendimentos (id_atendimento, id_cliente, id_guiche, data_hora_inicio, data_hora_fim, tempo_espera_min, sla_minutos, status_sla, motivo_chamada) VALUES (30, 28, 2, '2026-11-09 09:42:00', '2026-11-09 09:46:00', 9, 30, 'DENTRO', 'NORMAL');
COMMIT;

