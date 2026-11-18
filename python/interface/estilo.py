"""Identidade visual centralizada do Fila Justa."""
TEMAS = {
    "n4": {"icone": "👑", "cor": "#7c3aed", "fundo": "#ede9fe", "css": "n4"},
    "n3": {"icone": "🧓", "cor": "#2563eb", "fundo": "#dbeafe", "css": "n3"},
    "n2": {"icone": "♿", "cor": "#0d9488", "fundo": "#ccfbf1", "css": "n2"},
    "n1": {"icone": "🧑", "cor": "#475569", "fundo": "#e2e8f0", "css": "n1"},
}
def tema_categoria(categoria):
    nome = getattr(categoria, "name", "")
    return {"NIVEL_4":"n4","NIVEL_3":"n3","NIVEL_2":"n2","NIVEL_1":"n1"}.get(nome,"n1")

CSS = """
:root{--navy:#0f2a4a;--teal:#1d647a;--ink:#0f172a;--muted:#64748b;--line:#e2e8f0;--ok:#16a34a;--risco:#f59e0b;--estouro:#dc2626}
.stApp{background:linear-gradient(180deg,#eaf1f9 0%,#f7f9fc 55%);color:var(--ink)}
.block-container{padding-top:1rem;max-width:1360px}
header[data-testid="stHeader"]{background:transparent}
[data-testid="stSidebar"]{background:#f0f4f9;border-right:1px solid #dce5ef}
div.stButton>button,div.stDownloadButton>button{width:100%;border-radius:10px;font-weight:600;min-height:2.55rem}
.fj-hero{background:linear-gradient(120deg,#0f2a4a 0%,#1d647a 100%);color:#fff;border-radius:18px;padding:1.15rem 1.5rem;margin-bottom:.8rem;box-shadow:0 8px 24px rgba(15,42,74,.18);display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}
.fj-hero h1{margin:0;font-size:1.8rem;line-height:1.15;color:#fff}
.fj-hero p{margin:.3rem 0 0;opacity:.92;font-size:.95rem;color:#fff}
.fj-badges span{display:inline-block;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.28);padding:.2rem .65rem;border-radius:999px;font-size:.78rem;margin:.15rem .2rem 0 0;color:#fff}
div[data-testid="stRadio"] div[role="radiogroup"]{gap:.4rem;flex-wrap:wrap}
div[data-testid="stRadio"] div[role="radiogroup"]>label{background:#fff;border:1px solid var(--line);border-radius:999px;padding:.35rem .95rem;cursor:pointer;box-shadow:0 1px 2px rgba(15,23,42,.05)}
div[data-testid="stRadio"] div[role="radiogroup"]>label:has(input:checked){background:var(--navy);border-color:var(--navy)}
div[data-testid="stRadio"] div[role="radiogroup"]>label:has(input:checked) p{color:#fff}
div[data-testid="stRadio"] div[role="radiogroup"]>label>div:first-child{display:none}
.fj-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:.7rem;margin:.3rem 0 .85rem}
.fj-kpi{background:#fff;border:1px solid var(--line);border-left:5px solid var(--navy);border-radius:14px;padding:.65rem .9rem;box-shadow:0 1px 2px rgba(15,23,42,.05)}
.fj-kpi small{display:block;color:var(--muted);font-size:.7rem;text-transform:uppercase;letter-spacing:.05em}
.fj-kpi b{display:block;font-size:1.55rem;color:var(--ink);line-height:1.25}
.fj-kpi span{color:var(--muted);font-size:.75rem}
.fj-kpi.ok{border-left-color:var(--ok)}.fj-kpi.risco{border-left-color:var(--risco)}.fj-kpi.estouro{border-left-color:var(--estouro)}
.fj-card{--cat:#475569;--cat-bg:#e2e8f0;position:relative;display:grid;grid-template-columns:38px 1fr auto;gap:.25rem .7rem;align-items:center;background:#fff;border:1px solid var(--line);border-left:6px solid var(--cat);border-radius:14px;padding:.65rem .8rem;margin:.5rem 0;box-shadow:0 1px 2px rgba(15,23,42,.05)}
.fj-card.n4{--cat:#7c3aed;--cat-bg:#ede9fe}.fj-card.n3{--cat:#2563eb;--cat-bg:#dbeafe}.fj-card.n2{--cat:#0d9488;--cat-bg:#ccfbf1}.fj-card.n1{--cat:#475569;--cat-bg:#e2e8f0}
.fj-pos{width:34px;height:34px;border-radius:50%;background:var(--cat-bg);color:var(--cat);font-weight:800;display:flex;align-items:center;justify-content:center}
.fj-nome{font-weight:750;color:var(--ink)}.fj-meta{font-size:.78rem;color:var(--muted);margin-top:.12rem}
.fj-chip{display:inline-block;background:var(--cat-bg);color:var(--cat);padding:.08rem .5rem;border-radius:999px;font-size:.7rem;font-weight:700;margin-right:.3rem}
.fj-score{text-align:right}.fj-score b{font-size:1.1rem;color:var(--ink)}.fj-score small{display:block;color:var(--muted);font-size:.68rem}
.fj-proximo{border-color:#f59e0b;box-shadow:0 0 0 3px rgba(245,158,11,.22),0 5px 14px rgba(15,23,42,.08)}
.fj-ribbon{position:absolute;top:-9px;right:12px;background:#f59e0b;color:#fff;font-size:.65rem;font-weight:800;padding:.1rem .55rem;border-radius:999px;letter-spacing:.04em}
.fj-vazio{background:#fff;border:2px dashed #cbd5e1;border-radius:14px;padding:1.2rem;text-align:center;color:var(--muted);margin:.4rem 0}
.fj-aviso{border-radius:12px;padding:.7rem .9rem;margin:.35rem 0 .75rem;font-size:.88rem;background:#ecfeff;border:1px solid #a5f3fc;color:#155e75}
.fj-aviso.verde{background:#f0fdf4;border-color:#bbf7d0;color:#166534}
.fj-guiche{background:#fff;border:1px solid var(--line);border-radius:14px;padding:1rem;box-shadow:0 1px 2px rgba(15,23,42,.05);min-height:150px}
.fj-guiche.livre{border-top:5px solid #16a34a}.fj-guiche.ocupado{border-top:5px solid #f59e0b}
.fj-guiche h3{margin:0;color:var(--navy);font-size:1.05rem}.fj-guiche p{margin:.35rem 0;color:var(--muted);font-size:.85rem}
.fj-legenda{font-size:.78rem;color:var(--muted);margin:.3rem 0 .8rem}
@media(max-width:700px){.fj-hero{padding:1rem}.fj-hero h1{font-size:1.45rem}.fj-card{grid-template-columns:34px 1fr auto;padding:.55rem}.fj-score b{font-size:1rem}}
"""
