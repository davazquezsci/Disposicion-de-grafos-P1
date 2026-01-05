# Proyecto 5 – Disposición de grafos (Spring / Eades)

## Descripción general

En este proyecto se implementa un **algoritmo de disposición de grafos basado en fuerzas**
(**Spring Layout**, propuesto por P. Eades en 1984) para visualizar grafos generados a partir
de distintos **modelos clásicos de generación de grafos**.

Cada grafo es interpretado como un sistema físico:
- los **nodos** actúan como partículas,
- las **aristas** como resortes,
- y se aplican fuerzas de **atracción** y **repulsión** para obtener una configuración
geométrica estable.

El proyecto genera automáticamente **evidencia visual reproducible**
(imágenes y videos) para grafos de **100 y 500 nodos**, cumpliendo una complejidad
aproximada de **O(m + n)** por iteración.

## Objetivos

- Implementar el algoritmo **Spring (Eades, 1984)** desde cero.
- Visualizar grafos usando un motor propio basado en **pygame**.
- Analizar el comportamiento visual de distintos modelos de grafos.
- Generar evidencia automática y reproducible para evaluación.

## Modelos de grafos utilizados

1. Malla (Grid)
2. Erdős–Rényi
3. Gilbert
4. Geográfico
5. Barabási–Albert
6. Dorogovtsev–Mendes

Para cada modelo se generan dos instancias:
- **n = 100 nodos**
- **n = 500 nodos**

Total:
6 modelos × 2 tamaños = 12 grafos

## Algoritmo de disposición

El algoritmo modela el grafo como un sistema dinámico de fuerzas:
- atracción entre nodos conectados,
- repulsión entre nodos cercanos.

Se utiliza una aproximación por celdas espaciales para mantener una complejidad
aproximada **O(m + n)** por iteración.

## Estructura del proyecto
  Proyecto-5/
  │
  ├── lib/
  │ └── Biblioteca-grafos/ # Proyecto 1 (sin modificaciones)
  │
  ├── src/
  │ ├── grafo_layout.py # Implementación del Spring Layout
  │ └── viewer_pygame.py # Visualizador interactivo (pygame)
  │
  ├── scripts/
  │ ├── generar_grafos.py # Generación de grafos (12 casos)
  │ ├── correr_layout.py # Batch: layout + screenshots
  │ └── render_pygame.py # Visualización interactiva
  │
  ├── outputs/
  │ ├── data/
  │ │ └── layouts/ # Posiciones finales (JSON)
  │ │
  │ ├── img/
  │ │ ├── n100/ # Imágenes (100 nodos)
  │ │ └── n500/ # Imágenes (500 nodos)
  │ │
  │ └── videos/
  │ └── LINKS.md # Enlaces a videos
  │
  ├── README.md
  └── requirements.txt


## Uso

### Generar grafos
python scripts/generar_grafos.py

### Ejecutar layout y generar imágenes
python scripts/correr_layout.py

### Visualización interactiva
python scripts/render_pygame.py

## Evidencia

Las imágenes se almacenan en:
- outputs/img/n100
- outputs/img/n500

Los enlaces a videos se encuentran en:
- outputs/videos/LINKS.md

## Autor

Daniel Vázquez
Maestría en Ciencias de la Computación – IPN
