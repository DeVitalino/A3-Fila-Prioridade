import random

import pytest

from dominio.categoria import Categoria
from dominio.cliente import Cliente
from dominio.heap_binario import HeapBinario
from testes.auxiliar import SAQUE


def criar_cliente(id_cliente, categoria=Categoria.COMUM):
    return Cliente(id_cliente, f"X{id_cliente}", categoria, SAQUE, 0)


def test_remove_por_prioridade_da_categoria():
    heap = HeapBinario()
    heap.inserir(criar_cliente(1, Categoria.COMUM))
    heap.inserir(criar_cliente(2, Categoria.VIP))
    heap.inserir(criar_cliente(3, Categoria.PRIORITARIO))
    assert heap.remover().id_cliente == 3
    assert heap.remover().id_cliente == 2
    assert heap.remover().id_cliente == 1


def test_empate_resolvido_por_ordem_de_chegada():
    heap = HeapBinario()
    for i in (5, 2, 9, 1):
        heap.inserir(criar_cliente(i, Categoria.VIP))
    assert [heap.remover().id_cliente for _ in range(4)] == [1, 2, 5, 9]


def test_heap_com_muitos_itens_sai_ordenado():
    sorteio = random.Random(7)
    heap = HeapBinario()
    for i in range(1, 201):
        heap.inserir(criar_cliente(i, sorteio.choice(list(Categoria))))
    chaves = []
    while not heap.esta_vazio():
        chaves.append(heap.remover().chave())
    assert chaves == sorted(chaves)


def test_remover_cliente_do_meio_mantem_ordem():
    heap = HeapBinario()
    clientes = [criar_cliente(i, Categoria.COMUM) for i in range(1, 11)]
    for c in clientes:
        heap.inserir(c)
    heap.remover_cliente(clientes[4])
    ids = [heap.remover().id_cliente for _ in range(9)]
    assert ids == [1, 2, 3, 4, 6, 7, 8, 9, 10]


def test_reorganizar_depois_de_mudar_prioridade():
    heap = HeapBinario()
    comum = criar_cliente(1, Categoria.COMUM)
    vip = criar_cliente(2, Categoria.VIP)
    heap.inserir(comum)
    heap.inserir(vip)
    comum.prioridade_efetiva = -1
    heap.reorganizar()
    assert heap.espiar() is comum


def test_remover_de_fila_vazia_gera_erro():
    with pytest.raises(IndexError):
        HeapBinario().remover()
