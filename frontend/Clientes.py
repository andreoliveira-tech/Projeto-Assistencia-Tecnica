"""Ponto de entrada Streamlit com rótulo de navegação Clientes."""

from pathlib import Path
import runpy


# Reexecuta a página a cada rerun do Streamlit. Um import comum fica em cache e
# pode deixar a página inicial sem conteúdo após navegar entre páginas.
runpy.run_path(str(Path(__file__).with_name("app.py")), run_name="__main__")
