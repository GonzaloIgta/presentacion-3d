# Escenas: datos que acepta cada una

Todo va en `data` de la diapositiva. Convenciones comunes:

- `items` acepta strings (`"etiqueta"`) u objetos (`{"label": "etiqueta", ...}`).
- `shape` ∈ `box ico octa cone torus cyl sphere knot`. `tone` ∈ `hot ok bone`.
- `sub` es una segunda línea pequeña bajo la etiqueta. `text` sustituye el número mostrado por un texto propio (p. ej. `"9 €"`).
- Etiquetas 3D: 14–16 caracteres como mucho. Se encogen solas, pero largas se leen mal.
- Todo campo es opcional: sin `data`, cada escena pinta un ejemplo genérico.

## Portada, cierre y ambiente

| Escena | `data` |
|---|---|
| `orbit` | `shape`, `labels` (≤3, van en los satélites) |
| `morph` | `shapes`: lista de `sphere cube torus helix ring wave` (por defecto las cuatro primeras), `label` |
| `helix` | `labels` (2, una por hebra), `items` (≤5 etiquetas laterales que se encienden al pasar el pulso) |
| `wave` | `mode`: `waves` \| `ripple` \| `pulse`, `label` |
| `counter` | `value`, `from`, `dec`, `prefix`, `suffix`, `label`, `max` (si se da, el anillo se llena hasta `value/max`), `tone` |

## Procesos, pasos y causas

| Escena | `data` |
|---|---|
| `flow` | `items` (≤8 nodos, con `sub` y `shape` opcionales), `edges` (texto de cada flecha), `open: true` para línea en vez de ciclo |
| `stairs` | `items: [{label, sub}]` (≤8), `shape` del marcador |
| `timeline` | `items: [{label, sub}]` (≤8) |
| `gears` | `items: [{label, sub}]` (≤5) |
| `domino` | `items` (≤10 etiquetas) o `count` (2–14 fichas sin etiqueta). La última cae en color de acento |
| `rocket` | `items: [{label, sub}]` (≤5 hitos, de abajo arriba) |
| `funnel` | `items: [{label, value, text}]` (≤6, de mayor a menor). Con `value` muestra cifra y % sobre el primero |

## Datos y comparaciones

| Escena | `data` |
|---|---|
| `bars` | `items: [{label, value, text}]` (≤7). Negativos en `hot` |
| `line` | `items: [{label, value}]`, o `labels` + `series: [{name, values, tone}]` (≤3 series) |
| `donut` | `items: [{label, value, text, tone}]` (≤7), `center` (texto fijo; si falta, muestra el % del segmento resaltado) |
| `radar` | `items: [{label, value}]`, o `labels` (3–8 ejes) + `series: [{name, values, tone}]` (≤2), `max` (tope de la escala) |
| `gauge` | `items: [{label, value, min, max, dec, suffix, warn}]` (1–3). `max` por defecto 100; desde `warn` pinta en `hot` |
| `people` | `total` (≤100), `value`, `label`, `scatter: true` (encendidas salteadas), `tone`, `text` (sustituye «7 / 10») |
| `versus` | `left`, `right`: `{label, value, text, sub, shape}`, `metric` (rótulo superior) |
| `scatter` | `items: [{label, count, tone}]` (≤5 grupos; `count` = puntos del grupo, 4–70) |

## Estructura y relaciones

| Escena | `data` |
|---|---|
| `network` | `layers: [n, …]` (neuronas por capa), `outputs` (etiquetas de la última capa), `layerNames` |
| `hub` | `count` (productores), `hub` (nombre del centro), `shape` |
| `cards` | `items: [{label, tag, shape}]` (≤8). `tag: "hot"` resalta, `tag: "ok"` secundario |
| `tree` | `root`, `items: [{label, children: […]}]` (≤5 ramas, ≤4 hojas por rama) |
| `pyramid` | `items: [{label, sub}]` (≤6). El primero es la base |
| `layers` | `items: [{label, sub, tone}]` (≤6). El primero es la capa de arriba |
| `matrix` | `x`, `y` (nombres de los ejes), `quadrants` (4: arriba-izq, arriba-der, abajo-izq, abajo-der), `items: [{label, x, y, tone, shape}]` con `x`, `y` entre 0 y 1 (≤8), `focus` (0–3 fija el cuadrante resaltado) |
| `venn` | `items: [{label, sub, tone}]` (2–3 conjuntos), `center` (texto de la intersección) |
| `puzzle` | `items: [{label, tone}]` (≤9 piezas), `label` (rótulo que aparece al encajar) |
| `globe` | `items` (≤7 puntos sobre el globo) |

## Listas y temas concretos

| Escena | `data` |
|---|---|
| `list` | `items` (≤7), `mark: "check"` para ✓ (por defecto ✗) |
| `shield` | `label` (qué se protege), `shape`, `count` (atacantes, 1–12), `threats` (≤3 etiquetas sobre atacantes), `unit` (texto del contador, p. ej. `"bloqueados"`) |
| `dam` | `sensor`, `gate`, `attacker` (etiquetas). Ciclo de 20 s: normal → lectura falsificada → desborde → recuperación |

## Ejemplos mínimos

```json
{"scene": "radar", "title": "Dónde <em>ganamos</em>",
 "data": {"labels": ["precio", "calidad", "rapidez", "soporte", "diseño"],
          "series": [{"name": "nosotros", "values": [4, 5, 3, 4, 5]}, {"name": "rival", "values": [5, 3, 4, 2, 3]}]}}

{"scene": "counter", "title": "El <em>dato</em>",
 "data": {"value": 1284, "label": "clientes activos", "max": 2000}}

{"scene": "matrix", "title": "Qué hacer <em>primero</em>",
 "data": {"x": "esfuerzo", "y": "impacto", "quadrants": ["ya", "planificar", "si sobra", "descartar"],
          "items": [{"label": "suscripción", "x": 0.3, "y": 0.85}, {"label": "franquicia", "x": 0.8, "y": 0.25}]}}

{"scene": "gauge", "title": "Cómo <em>vamos</em>",
 "data": {"items": [{"label": "objetivo", "value": 82, "suffix": " %"},
                    {"label": "mermas", "value": 7, "max": 10, "warn": 6, "suffix": " %"}]}}
```
