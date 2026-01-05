from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ============================================================
# Proyecto 1: Biblioteca-grafos
# ============================================================
P1_SRC = ROOT / "lib" / "Biblioteca-grafos" / "src"
sys.path.insert(0, str(P1_SRC))

# --- compat: la biblioteca espera "src.grafo" ---
# (porque modelos.py hace: from src.grafo import Grafo)
import types, importlib  # noqa: E402

pkg = types.ModuleType("src")
sys.modules["src"] = pkg
sys.modules["src.grafo"] = importlib.import_module("grafo")

import modelos  # noqa: E402

# ============================================================
# Output
# ============================================================
OUT_GV = ROOT / "outputs" / "gv" / "generados"
OUT_GV.mkdir(parents=True, exist_ok=True)


def main():
    # 6 modelos × {100, 500}  => 12 grafos
    # (nombre, builder)
    casos = [
        # Malla: 100 ~ 10x10; 500 ~ 20x25
        ("malla_n100", lambda: modelos.grafoMalla(10, 10, dirigido=False)),
        ("malla_n500", lambda: modelos.grafoMalla(20, 25, dirigido=False)),

        # Erdős–Rényi: m ~ 2n (sparse)
        ("erdos_n100", lambda: modelos.grafoErdosRenyi(100, 200, False, seed=1)),
        ("erdos_n500", lambda: modelos.grafoErdosRenyi(500, 1000, False, seed=2)),

        # Gilbert: p ajustado para densidad moderada
        ("gilbert_n100", lambda: modelos.grafoGilbert(100, 0.04, False, seed=1)),
        ("gilbert_n500", lambda: modelos.grafoGilbert(500, 0.01, False, seed=2)),

        # Geográfico: r ajustado
        ("geo_n100", lambda: modelos.grafoGeografico(100, 0.18, False, seed=1)),
        ("geo_n500", lambda: modelos.grafoGeografico(500, 0.10, False, seed=2)),

        # Barabási–Albert: d=3
        ("ba_n100", lambda: modelos.grafoBarabasiAlbert(100, 3, False, seed=1)),
        ("ba_n500", lambda: modelos.grafoBarabasiAlbert(500, 3, False, seed=2)),

        # Dorogovtsev–Mendes
        ("dm_n100", lambda: modelos.grafoDorogovtsevMendes(100, False, seed=1)),
        ("dm_n500", lambda: modelos.grafoDorogovtsevMendes(500, False, seed=2)),
    ]

    for nombre, builder in casos:
        g = builder()
        out_path = OUT_GV / f"{nombre}.gv"
        g.to_graphviz(str(out_path))
        print("[OK]", nombre, "->", out_path)


if __name__ == "__main__":
    main()
