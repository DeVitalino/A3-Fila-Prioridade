"""Componentes HTML puros e seguros."""
import html, re
from .estilo import TEMAS, tema_categoria

def esc(valor):
    return html.escape(str(valor), quote=True).replace("$","&#36;")

def minificar(codigo):
    return re.sub(r">\s+<", "><", " ".join(codigo.split()))

def hero(titulo, subtitulo, etiquetas):
    chips="".join(f"<span>{esc(x)}</span>" for x in etiquetas)
    return minificar(f'<div class="fj-hero"><div><h1>{esc(titulo)}</h1><p>{esc(subtitulo)}</p></div><div class="fj-badges">{chips}</div></div>')

def kpis(itens):
    corpo="".join(f'<div class="fj-kpi {esc(i.get("tom",""))}"><small>{esc(i["titulo"])}</small><b>{esc(i["valor"])}</b><span>{esc(i.get("detalhe",""))}</span></div>' for i in itens)
    return minificar(f'<div class="fj-kpis">{corpo}</div>')

def aviso(texto, tom=""):
    return minificar(f'<div class="fj-aviso {esc(tom)}">{texto}</div>')

def vazio(texto):
    return minificar(f'<div class="fj-vazio">🗂️ {esc(texto)}</div>')

def cartao_cliente(cliente, posicao, espera, sla, destaque=False):
    tema=tema_categoria(cliente.categoria); dados=TEMAS[tema]
    classe="fj-card "+tema+(" fj-proximo" if destaque else "")
    faixa='<div class="fj-ribbon">PRÓXIMO A SER CHAMADO</div>' if destaque else ""
    pontos="Prioridade absoluta" if tema=="n4" else f'{cliente.pontuacao_atual:.2f} pontos'
    formula="" if tema=="n4" else f'<div class="fj-meta">Pontuação: {esc(cliente.pontuacao_inicial)} × 1,6 por período completo de 20 min</div>'
    return minificar(f'<div class="{classe}">{faixa}<div class="fj-pos">{posicao}</div><div><div class="fj-nome">{dados["icone"]} {esc(cliente.senha)} <span style="font-weight:500;color:#64748b">· {esc(cliente.categoria.nome_curto)}</span></div><div class="fj-meta">{esc(cliente.idade)} anos · {esc(cliente.tipo_servico.nome)} · Espera: {esc(espera)} min · SLA: {esc(sla)} min</div>{formula}</div><div class="fj-score"><b>{esc(pontos)}</b><small>pontuação atual</small></div></div>')

def guiche(numero, cliente, restante, total):
    if cliente is None:
        return minificar(f'<div class="fj-guiche livre"><h3>🪟 Guichê {esc(numero)}</h3><p>🟢 Disponível para atendimento</p><p>Total de atendimentos: {esc(total)}</p></div>')
    return minificar(f'<div class="fj-guiche ocupado"><h3>🪟 Guichê {esc(numero)}</h3><p>🟠 Em atendimento</p><p><b>{esc(cliente.senha)}</b> · {esc(cliente.tipo_servico.nome)}</p><p>Tempo restante: {esc(restante)} min</p><p>Total de atendimentos: {esc(total)}</p></div>')
