# Notas da atualização visual

- A interface principal agora usa o design system Fila Justa.
- A implementação antiga em `ui/painel_streamlit.py` foi preservada como referência, mas o ponto de entrada `trabalhoA3.py` agora direciona para `app.py`.
- As regras de domínio, serviços, repositórios, configuração e persistência não foram alteradas.
- A aplicação exige as dependências listadas em `requirements.txt` dentro da pasta `python`.
- Execução: entre em `python/`, instale `pip install -r requirements.txt` e execute `streamlit run trabalhoA3.py`.
