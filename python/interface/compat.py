"""Helpers para compatibilidade entre versões do Streamlit."""
import streamlit as st

def com_largura_total(funcao, *args, **kwargs):
    try:
        return funcao(*args, **kwargs, width="stretch")
    except TypeError:
        return funcao(*args, **kwargs, use_container_width=True)
