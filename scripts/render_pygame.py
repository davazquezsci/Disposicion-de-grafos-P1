from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ============================================================
# Proyecto 5: módulos locales (mismo patrón que Proyecto 4)
#   - Importamos como módulos planos desde ROOT/src:
#       from grafo_layout import ...
#       from viewer_pygame import ...
# ============================================================
sys.path.insert(0, str(ROOT / "src"))

from grafo_layout import spring_eades_layout, SpringParams
from viewer_pygame import PygameViewer


# ============================================================
# Proyecto 1: Biblioteca-grafos
# ============================================================
P1_SRC = ROOT / "lib" / "Biblioteca-grafos" / "src"
sys.path.insert(0, str(P1_SRC))

# --- compat: la biblioteca espera "src.grafo" ---
# modelos.py trae: from src.grafo import Grafo
# sin modificar la biblioteca, creamos el alias en runtime
import types, importlib  # noqa: E402

pkg = types.ModuleType("src")
sys.modules["src"] = pkg
sys.modules["src.grafo"] = importlib.import_module("grafo")

import modelos  # noqa: E402


def main():
    g = modelos.grafoErdosRenyi(100, 200, False, seed=1)

    params = SpringParams(
        c2=120.0,
        cell_size=140.0,
        iters=200,
        max_disp=10.0,
    )

    pos = spring_eades_layout(g, width=1200, height=800, seed=1, params=params)

    viewer = PygameViewer(g, pos, width=1200, height=800, title="Spring (Eades) - n=100")
    viewer.run(screenshot_dir=str(ROOT / "outputs" / "img"))


if __name__ == "__main__":
    main()
