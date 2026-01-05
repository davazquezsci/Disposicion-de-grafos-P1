from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ============================================================
# Proyecto 5: módulos locales (estilo Proyecto 4)
# ============================================================
sys.path.insert(0, str(ROOT / "src"))
from grafo_layout import spring_eades_layout, SpringParams, save_layout_json  # noqa: E402

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
# Outputs
# ============================================================
OUT_LAYOUTS = ROOT / "outputs" / "data" / "layouts"
OUT_IMG_100 = ROOT / "outputs" / "img" / "n100"
OUT_IMG_500 = ROOT / "outputs" / "img" / "n500"

OUT_LAYOUTS.mkdir(parents=True, exist_ok=True)
OUT_IMG_100.mkdir(parents=True, exist_ok=True)
OUT_IMG_500.mkdir(parents=True, exist_ok=True)


def render_png_pygame(g, pos, out_png: Path, width: int, height: int, node_r: int):
    """
    Render estático a PNG usando pygame (sin interacción).
    """
    import pygame  # import local para no exigir pygame si solo quieres layouts

    pygame.init()
    # Ventana oculta (en Windows funciona bien para batch)
    screen = pygame.display.set_mode((width, height), flags=pygame.HIDDEN)

    screen.fill((16, 16, 18))

    # aristas
    for e in g.aristas():
        u = e.origen.id
        v = e.destino.id
        if u not in pos or v not in pos:
            continue
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        pygame.draw.line(screen, (120, 120, 130), (x1, y1), (x2, y2), 1)

    # nodos
    for n in g.nodos():
        nid = n.id
        if nid not in pos:
            continue
        x, y = pos[nid]
        pygame.draw.circle(screen, (240, 240, 245), (int(x), int(y)), node_r)

    pygame.image.save(screen, str(out_png))
    pygame.quit()


def casos():
    # 6 modelos × {100, 500}
    return [
        ("malla_n100", 100, lambda: modelos.grafoMalla(10, 10, dirigido=False)),
        ("malla_n500", 500, lambda: modelos.grafoMalla(20, 25, dirigido=False)),

        ("erdos_n100", 100, lambda: modelos.grafoErdosRenyi(100, 200, False, seed=1)),
        ("erdos_n500", 500, lambda: modelos.grafoErdosRenyi(500, 1000, False, seed=2)),

        ("gilbert_n100", 100, lambda: modelos.grafoGilbert(100, 0.04, False, seed=1)),
        ("gilbert_n500", 500, lambda: modelos.grafoGilbert(500, 0.01, False, seed=2)),

        ("geo_n100", 100, lambda: modelos.grafoGeografico(100, 0.18, False, seed=1)),
        ("geo_n500", 500, lambda: modelos.grafoGeografico(500, 0.10, False, seed=2)),

        ("ba_n100", 100, lambda: modelos.grafoBarabasiAlbert(100, 3, False, seed=1)),
        ("ba_n500", 500, lambda: modelos.grafoBarabasiAlbert(500, 3, False, seed=2)),

        ("dm_n100", 100, lambda: modelos.grafoDorogovtsevMendes(100, False, seed=1)),
        ("dm_n500", 500, lambda: modelos.grafoDorogovtsevMendes(500, False, seed=2)),
    ]


def main():
    W, H = 1200, 800

    # parámetros del layout (puedes ajustar después)
    params_100 = SpringParams(c2=120.0, cell_size=140.0, iters=250, max_disp=10.0)
    params_500 = SpringParams(c2=90.0,  cell_size=110.0, iters=300, max_disp=8.0)

    for nombre, n, builder in casos():
        g = builder()

        params = params_100 if n == 100 else params_500
        seed = 1 if n == 100 else 2

        pos = spring_eades_layout(g, width=W, height=H, seed=seed, params=params)

        # guardar posiciones
        out_json = OUT_LAYOUTS / f"{nombre}.json"
        save_layout_json(str(out_json), pos, meta={"name": nombre, "n": n, "W": W, "H": H})
        print("[OK] layout:", nombre, "->", out_json)

        # screenshot
        out_dir = OUT_IMG_100 if n == 100 else OUT_IMG_500
        out_png = out_dir / f"{nombre}.png"
        node_r = 3 if n == 100 else 2
        render_png_pygame(g, pos, out_png, width=W, height=H, node_r=node_r)
        print("[OK] png   :", nombre, "->", out_png)


if __name__ == "__main__":
    main()
