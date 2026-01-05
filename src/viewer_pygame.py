from __future__ import annotations

import os
import time
from typing import Any, Dict, Tuple

import pygame

Vec2 = Tuple[float, float]


class PygameViewer:
    def __init__(
        self,
        g,
        pos: Dict[Any, Vec2],
        width: int = 1200,
        height: int = 800,
        title: str = "Proyecto 5 - Spring (Eades) - Viewer",
    ):
        self.g = g
        self.pos = pos
        self.W = width
        self.H = height

        self.title = title

        # cámara
        self.offset = pygame.Vector2(0, 0)
        self.zoom = 1.0

        # dragging
        self.dragging = False
        self.last_mouse = pygame.Vector2(0, 0)

    def world_to_screen(self, p: Vec2) -> pygame.Vector2:
        v = pygame.Vector2(p[0], p[1])
        v = (v + self.offset) * self.zoom
        return v

    def run(self, screenshot_dir: str = "outputs/img", node_radius: int = 3):
        pygame.init()
        screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption(self.title)
        clock = pygame.time.Clock()

        os.makedirs(screenshot_dir, exist_ok=True)

        running = True
        while running:
            dt = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.dragging = True
                        self.last_mouse = pygame.Vector2(*event.pos)
                    elif event.button == 4:  # wheel up
                        self.zoom *= 1.1
                    elif event.button == 5:  # wheel down
                        self.zoom /= 1.1
                        if self.zoom < 0.1:
                            self.zoom = 0.1

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        m = pygame.Vector2(*event.pos)
                        delta = (m - self.last_mouse) / max(self.zoom, 1e-6)
                        self.offset += delta
                        self.last_mouse = m

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_s:
                        ts = time.strftime("%Y%m%d_%H%M%S")
                        path = os.path.join(screenshot_dir, f"screenshot_{ts}.png")
                        pygame.image.save(screen, path)
                        print("[OK] screenshot:", path)

            # draw
            screen.fill((16, 16, 18))

            # edges
            for e in self.g.aristas():
                u = e.origen.id
                v = e.destino.id
                if u not in self.pos or v not in self.pos:
                    continue
                pu = self.world_to_screen(self.pos[u])
                pv = self.world_to_screen(self.pos[v])
                pygame.draw.line(screen, (120, 120, 130), pu, pv, 1)

            # nodes
            for n in self.g.nodos():
                nid = n.id
                if nid not in self.pos:
                    continue
                p = self.world_to_screen(self.pos[nid])
                pygame.draw.circle(screen, (240, 240, 245), p, node_radius)

            pygame.display.flip()

        pygame.quit()
