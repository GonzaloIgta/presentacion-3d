---
name: presentacion-3d
description: Crea presentaciones web 3D animadas (Three.js, un HTML que se abre con doble clic, sin servidor) sobre cualquier temática, con un estilo propio: fondo oscuro, HUD, tipografía condensada, una escena 3D viva por diapositiva (33 disponibles) y navegación por teclado. Úsala cuando el usuario pida una presentación, informe, charla o slides "3D", "animadas", dándote el tema y/o los apartados.
---

# Presentación 3D

Genera una presentación a partir de un **spec JSON**. Cada diapositiva = texto a un lado + una **escena 3D animada** al otro. El motor y las 33 escenas ya están hechos (`assets/template.html`); tú solo escribes el contenido.

`<skill>` en los comandos es la carpeta de esta skill (`~/.claude/skills/presentacion-3d`).

## Flujo

1. **Entender el pedido.** Tema, audiencia, apartados e idioma. Si no hay apartados, proponlos (8–12 diapositivas). Pregunta solo si falta algo que cambia el resultado (tema o idioma); lo demás, decide con criterio.
2. **Elegir escenas** con la tabla «Qué quiero contar» de abajo. Los datos exactos de cada una están en `references/escenas.md`: léelo para las escenas que vayas a usar.
3. **Escribir el spec** (p. ej. `presentaciones/<tema>/spec.json`). Ejemplos completos: `examples/demo.json` y `examples/demo-animaciones.json`.
4. **Construir:**
   ```bash
   python <skill>/scripts/build.py spec.json salida/presentacion.html
   ```
   Lee los `AVISO:` que imprime (items de más, etiquetas largas, escena repetida) y corrige el spec.
5. **Comprobar siempre**, antes de entregar:
   ```bash
   python <skill>/scripts/check.py salida/presentacion.html --shots salida/capturas
   ```
   Abre el HTML como `file://` en Edge/Chrome sin ventana, simula 30 s de cada escena y lista las que fallan. Con `--shots` deja una captura por diapositiva: míralas (encuadre, texto pisado, etiquetas cortadas) y ajusta. No entregues con errores ni sin haber visto las capturas; si no hay navegador, dilo.
6. **Entregar:** ruta del HTML, atajos de teclado y qué escena usa cada apartado.

Opciones de `build.py`:

- `--single` incrusta three.js en el HTML: **un único fichero** para enviar por correo o chat. Sin ella, `three.min.js` se copia al lado y deben viajar juntos.
- `--gallery salida/galeria.html` construye una presentación con una diapositiva por escena. Úsala para enseñar el catálogo al usuario o para ver una escena antes de elegirla.
- `--list` imprime las escenas y para qué sirve cada una.

## Formato del spec

```json
{
  "title": "Título de la pestaña",
  "hud": "Texto de la esquina superior izquierda",
  "lang": "es",
  "theme": {"hot": "#ff5a1f", "ok": "#a3b565"},
  "autoSeconds": 15,
  "intro": "auto",
  "slides": [ { "scene": "orbit", "title": "…", "data": { } } ]
}
```

- `lang`: `es` | `en` (textos de interfaz).
- `theme` (opcional): `hot` = acento principal, `ok` = acento secundario; también `ink`, `bone`, `dim`, `rule`. Mantener `ink` oscuro.
- `autoSeconds`: segundos por diapositiva en modo auto (tecla P).
- `intro`: animación de entrada de las escenas (ver abajo).

### Diapositiva

| Campo | Descripción |
|---|---|
| `scene` | nombre de la escena (tabla de abajo) |
| `data` | datos de la escena (`references/escenas.md`) |
| `kicker` | etiqueta pequeña sobre el título |
| `title` | título; `<br>` parte líneas, `<em>…</em>` lo pinta en color de acento. Máx. ~3 líneas cortas |
| `text` | párrafo breve (1–2 frases) |
| `rows` | `[["Término","explicación"], …]` lista de definiciones (3–5 filas; `<b>` resalta) |
| `stats` | `[{"value":62.5,"dec":1,"suffix":" %","label":"victorias","tone":"ok"}]` contadores animados (2–3) |
| `note` | nota discreta al pie, visible para el público |
| `notes` | notas del orador: ocultas, se muestran con la tecla N |
| `side` | `"right"` pone el texto a la derecha y la escena a la izquierda |
| `hero` | `true` usa título grande sin número (por defecto solo la primera) |
| `intro` | animación de entrada solo para esta diapositiva |
| `cam`, `look` | opcional: `[x,y,z]` para recolocar cámara y objetivo |

Los textos aceptan HTML mínimo (`<b>`, `<em>`, `<br>`). Los números de diapositiva son automáticos.

## Qué quiero contar → qué escena

| Quiero contar… | Escenas |
|---|---|
| Portada, cierre, idea central | `orbit` `morph` `helix` `globe` |
| El dato estrella | `counter` `people` `gauge` |
| Un proceso o ciclo | `flow` `gears` `stairs` |
| Causa → efecto, dependencias (interactiva) | `domino` `flow` (con `open`) |
| Tiempo, hitos, lanzamiento | `timeline` `rocket` `stairs` |
| Comparar valores | `bars` `radar` `versus` `line` |
| Reparto de un total | `donut` `people` `funnel` |
| Evolución o tendencia | `line` `wave` |
| Pérdidas por etapas | `funnel` |
| Jerarquía o prioridades | `pyramid` `tree` `matrix` |
| Arquitectura, capas, componentes | `layers` `network` `hub` `cards` |
| Lo que tienen en común, integración | `venn` `puzzle` `gears` |
| Grupos, segmentos | `scatter` `cards` |
| Alcance geográfico | `globe` |
| Seguridad, riesgo | `shield` `gauge` `dam` |
| Descartado / conseguido | `list` |
| Ambiente sin datos | `wave` `morph` |

`python <skill>/scripts/build.py --list` da la descripción de una línea de cada una.

## Animación de entrada (`intro`)

Además de la animación propia de cada escena, el bloque 3D puede entrar animado. En la raíz del spec vale para todas; en una diapositiva, solo para esa.

`none` (por defecto) · `rise` sube del suelo · `drop` cae · `zoom` crece · `spin` entra girando · `slide` entra de lado · `flip` se levanta · `auto` una distinta por diapositiva.

## Criterios de calidad

- **Una idea por diapositiva.** Texto corto: la escena cuenta lo visual, el texto lo esencial. Títulos de 2–3 palabras por línea, con una palabra clave en `<em>`.
- **Escena acorde al contenido**: elige por la tabla, no al azar. Con 33 escenas no hace falta repetir: como mucho una escena dos veces por presentación.
- **Ritmo**: alterna `side` en 1 de cada 3–4. Las escenas anchas (`tree`, `line`, `gears`, `domino`, `timeline`, `gauge` con 3) van mejor sin `side:"right"` y con título corto.
- **Etiquetas 3D cortas** (≤ 14 caracteres). Respeta los máximos de items de `references/escenas.md`; `build.py` avisa si te pasas.
- **Datos reales cuando existan**; si son ilustrativos, dilo en `note`.
- **Paleta al tema**: cambia `theme.hot/ok` (azul/cian para océano, ámbar/verde para energía…) para que no todas parezcan la misma.
- **Estructura típica**: portada (`orbit`/`morph`) → contexto (`counter`/`globe`) → mecanismo (`flow`/`layers`) → fases (`stairs`/`timeline`) → resultados (`bars`/`line` + `stats`) → decisión (`matrix`/`versus`) → cierre (`helix`/`rocket`).

## Interactividad

Algunas escenas reaccionan al ratón (hover = pasar el cursor, clic): `domino` (clic en una ficha lanza la cadena desde ahí), `network` (hover ilumina neuronas, clic lanza una pasada), `layers` (hover resalta la capa, clic separa la pila), `bars` (hover alza la barra, clic la hace saltar) y `cards` (hover agranda, clic hace girar). Para añadirlo a otra escena: `hit(mesh,{over,out,click})` en el motor; el cursor cambia a mano solo.

## Controles de la presentación

`←` `→` / espacio navegar · `O` índice · `P` modo auto · `N` notas del orador · `F` pantalla completa · `Home/End` · deslizar en móvil · URL `#N` abre la diapositiva N.

## Ampliar el motor

Para una escena nueva:

1. Añadir `SCENES.nombre=(g,data)=>({cam,look,enter?,update(dt,t,s)})` en `assets/template.html`. Ayudas disponibles: `M()`, `shape()`, `label()`, `burst()`, `ringMesh()`, `pedestal()`, `itemsOf()`, `toneOf()`, `glow()`, `poly()`. `t` es el tiempo global, `s` los segundos desde que se entró en la diapositiva.
2. Registrarla en `SCENES` de `scripts/build.py` (descripción y máximo de items), y un ejemplo en `SAMPLES` si sus valores por defecto no lucen.
3. Documentar sus datos en `references/escenas.md` y añadirla a la tabla «Qué quiero contar».
4. Probarla con `build.py --gallery` + `check.py --shots`.

Reglas del motor que una escena debe respetar:

- Toda escena debe pintar algo razonable con `data` vacío.
- `burst()` trabaja en coordenadas de mundo: para un objeto dentro de un grupo girado, usar `obj.getWorldPosition(V)`.
- `update` no debe crear objetos ni geometrías en cada fotograma (solo mover, escalar, cambiar colores).
- Si una escena lanza un error, el motor lo escribe en consola con el prefijo `[presentacion-3d]`, congela esa escena y sigue; `check.py` lo detecta.

