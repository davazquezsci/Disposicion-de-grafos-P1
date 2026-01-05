from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from typing import Dict, Tuple, Any, Iterable


Vec2 = Tuple[float, float]


@dataclass
class SpringParams:
    # constantes estilo Eades
    c1: float = 2.0      # atracción
    c2: float = 120.0    # distancia "ideal" (en pixels)
    c3: float = 1.0      # repulsión
    c4: float = 0.10     # paso (learning rate)
    iters: int = 150

    # estabilidad
    max_disp: float = 10.0   # clamp del movimiento por iteración (pixels)
    eps: float = 1e-6

    # grid para aproximar repulsión (O(n))
    cell_size: float = 140.0      # ~ cercano a c2
    neighbor_radius: int = 1      # 1 => 3x3 celdas, 2 => 5x5


def _clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else (hi if x > hi else x)


def _add(a: Vec2, b: Vec2) -> Vec2:
    return (a[0] + b[0], a[1] + b[1])


def _sub(a: Vec2, b: Vec2) -> Vec2:
    return (a[0] - b[0], a[1] - b[1])


def _mul(a: Vec2, k: float) -> Vec2:
    return (a[0] * k, a[1] * k)


def _norm(a: Vec2) -> float:
    return math.hypot(a[0], a[1])


def _unit(a: Vec2, eps: float) -> Vec2:
    d = _norm(a)
    if d < eps:
        return (0.0, 0.0)
    return (a[0] / d, a[1] / d)


def _grid_key(p: Vec2, cell: float) -> Tuple[int, int]:
    return (int(p[0] // cell), int(p[1] // cell))


def _iter_neighbor_cells(cx: int, cy: int, r: int) -> Iterable[Tuple[int, int]]:
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            yield (cx + dx, cy + dy)


def spring_eades_layout(
    g,
    width: int = 1200,
    height: int = 800,
    seed: int = 123,
    params: SpringParams | None = None,
) -> Dict[Any, Vec2]:
    """
    Calcula posiciones 2D con un layout tipo Eades (1984):
    - atracción (aristas):  F_a(d) = c1 * log(d/c2)
    - repulsión (aprox grid): ~ c3 / sqrt(d) (como forma típica en el survey)
    - actualización: pos += c4 * F , con clamp para estabilidad

    O(m+n) por iteración (aprox), usando grid hashing para repulsión local.
    """
    if params is None:
        params = SpringParams()

    rng = random.Random(seed)

    # ids de nodos (tu Grafo usa Nodo.id)
    nodes = g.nodos()
    ids = [n.id for n in nodes]
    n = len(ids)
    if n == 0:
        return {}

    # posiciones iniciales:
    # - si el grafo ya tiene x,y (ej. geográfico), respetamos pero escalamos a pantalla
    # - si no, aleatorias dentro del canvas
    pos: Dict[Any, Vec2] = {}
    has_any_coords = any((getattr(n, "x", None) is not None and getattr(n, "y", None) is not None) for n in nodes)

    if has_any_coords:
        # coords típicamente en [0,1]x[0,1], los convertimos a pixels
        for nd in nodes:
            if nd.x is None or nd.y is None:
                x = rng.uniform(0.0, width)
                y = rng.uniform(0.0, height)
            else:
                x = float(nd.x) * (width - 40) + 20
                y = float(nd.y) * (height - 40) + 20
            pos[nd.id] = (x, y)
    else:
        for nd in nodes:
            pos[nd.id] = (rng.uniform(0.0, width), rng.uniform(0.0, height))

    # Precomputar lista de aristas como pares (u_id, v_id)
    # Ojo: tu Grafo expone aristas() pero también _aristas_key; usamos aristas() limpio
    edges = []
    for e in g.aristas():
        edges.append((e.origen.id, e.destino.id))

    # loop principal
    for _ in range(params.iters):
        # fuerzas netas
        force: Dict[Any, Vec2] = {i: (0.0, 0.0) for i in ids}

        # --------------------------
        # 1) Repulsión (aprox O(n))
        # --------------------------
        grid: Dict[Tuple[int, int], list[Any]] = {}
        cell = params.cell_size

        for i in ids:
            key = _grid_key(pos[i], cell)
            grid.setdefault(key, []).append(i)

        for i in ids:
            pi = pos[i]
            cx, cy = _grid_key(pi, cell)

            fx, fy = force[i]
            for nk in _iter_neighbor_cells(cx, cy, params.neighbor_radius):
                if nk not in grid:
                    continue
                for j in grid[nk]:
                    if j == i:
                        continue
                    pj = pos[j]
                    dvec = _sub(pi, pj)
                    d = _norm(dvec) + params.eps

                    # repulsión tipo c3 / sqrt(d)
                    mag = params.c3 / math.sqrt(d)
                    u = (dvec[0] / d, dvec[1] / d)  # unit
                    fx += u[0] * mag
                    fy += u[1] * mag
            force[i] = (fx, fy)

        # --------------------------
        # 2) Atracción por aristas O(m)
        # --------------------------
        for (u, v) in edges:
            pu = pos[u]
            pv = pos[v]
            dvec = _sub(pv, pu)
            d = _norm(dvec) + params.eps
            uvec = (dvec[0] / d, dvec[1] / d)

            # F_a(d) = c1 * log(d/c2)
            mag = params.c1 * math.log(d / params.c2)

            # aplicar fuerzas opuestas
            fu = force[u]
            fv = force[v]
            force[u] = (fu[0] + uvec[0] * mag, fu[1] + uvec[1] * mag)
            force[v] = (fv[0] - uvec[0] * mag, fv[1] - uvec[1] * mag)

        # --------------------------
        # 3) Actualización posiciones
        # --------------------------
        for i in ids:
            fx, fy = force[i]
            disp = (fx * params.c4, fy * params.c4)

            # clamp del desplazamiento
            d = _norm(disp)
            if d > params.max_disp:
                disp = _mul(_unit(disp, params.eps), params.max_disp)

            x, y = pos[i]
            x = _clamp(x + disp[0], 0.0, float(width))
            y = _clamp(y + disp[1], 0.0, float(height))
            pos[i] = (x, y)

    return pos


def save_layout_json(path: str, pos: Dict[Any, Vec2], meta: dict | None = None) -> None:
    data = {
        "meta": meta or {},
        "pos": {str(k): [float(v[0]), float(v[1])] for k, v in pos.items()},
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_layout_json(path: str) -> Dict[Any, Vec2]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    out: Dict[Any, Vec2] = {}
    for k, v in data["pos"].items():
        out[k] = (float(v[0]), float(v[1]))
    return out
