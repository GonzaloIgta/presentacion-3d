#!/usr/bin/env python3
"""Genera una presentación 3D (HTML + three.min.js) a partir de un spec JSON.

Uso:
  python build.py spec.json salida/presentacion.html [--single]
  python build.py --gallery salida/galeria.html [--single]   una diapositiva por escena, para elegir
  python build.py --list                                      lista las escenas y para qué sirven

--single  incrusta three.min.js dentro del HTML: un único fichero para enviar por correo o chat.
Sin --single se copia three.min.js junto al HTML (deben viajar juntos).
Los avisos (demasiados items, etiquetas largas...) salen por stderr y no detienen la construcción.
"""
import json, shutil, sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# nombre -> (para qué sirve, máximo de items que se leen bien o None)
SCENES = {
    "orbit": ("portada o cierre: figura central con anillos y satélites", None),
    "flow": ("ciclos, pipelines, procesos, causa -> efecto", 8),
    "bars": ("comparar valores; los negativos en color de acento", 7),
    "stairs": ("fases, niveles, progresión", 8),
    "network": ("red por capas: entradas -> decisiones", None),
    "cards": ("catálogo, equipo, categorías", 8),
    "hub": ("varias fuentes hacia un centro, paralelismo", None),
    "timeline": ("cronología, roadmap, hitos", 8),
    "list": ("descartado (x) o conseguido (check)", 7),
    "dam": ("simulación de ataque a una presa (sensor -> PLC -> compuerta)", None),
    "globe": ("alcance global, sedes, rutas", 7),
    "donut": ("reparto de un total, cuotas", 7),
    "line": ("tendencias y evolución; hasta 3 series", 10),
    "funnel": ("conversión por etapas", 6),
    "gauge": ("1-3 indicadores de aguja: KPI, avance, riesgo", 3),
    "people": ("pictograma: N de cada M", None),
    "versus": ("A frente a B en una balanza", None),
    "gears": ("engranajes: piezas que dependen unas de otras", 5),
    "tree": ("organigrama, desglose, taxonomía", 5),
    "pyramid": ("jerarquía, prioridades (primer item = base)", 6),
    "matrix": ("matriz 2x2: priorización, DAFO", 8),
    "helix": ("doble hélice: dos fuerzas entrelazadas", 5),
    "wave": ("ambiente: campo de barras que ondula", None),
    "radar": ("gráfico de araña: comparar varios ejes; hasta 2 series", 8),
    "layers": ("pila de capas: arquitectura, stack (primer item = arriba)", 6),
    "scatter": ("nube de puntos que se ordena en grupos: segmentación", 5),
    "venn": ("2-3 discos que se solapan: lo que tienen en común", 3),
    "counter": ("cifra gigante que cuenta: el dato estrella", None),
    "morph": ("partículas que cambian de figura: transformación, portada", None),
    "domino": ("fichas que caen en cadena: causa -> efecto, dependencias", 10),
    "puzzle": ("piezas que encajan: integración, el todo y las partes", 9),
    "shield": ("escudo que bloquea ataques: seguridad, resiliencia", None),
    "rocket": ("cohete que atraviesa hitos: lanzamiento, crecimiento", 5),
}
INTROS = {"none", "auto", "rise", "drop", "zoom", "spin", "slide", "flip"}
WIDE = {"tree", "line", "gears", "domino", "timeline"}  # ocupan mucho ancho: pisan el texto con side:right
LABEL_MAX = 16

# datos de muestra para la galería (las escenas que no aparecen usan sus valores por defecto)
SAMPLES = {
    "orbit": {"labels": ["uno", "dos", "tres"]},
    "counter": {"value": 1284, "label": "clientes", "max": 2000},
    "people": {"total": 10, "value": 7, "label": "repiten"},
    "versus": {"metric": "coste", "left": {"label": "antes", "value": 9}, "right": {"label": "ahora", "value": 5}},
    "gauge": {"items": [{"label": "avance", "value": 72, "suffix": " %"}, {"label": "riesgo", "value": 8, "max": 10, "warn": 6}]},
    "tree": {"root": "raíz", "items": [{"label": "rama A", "children": ["a1", "a2"]}, {"label": "rama B", "children": ["b1", "b2", "b3"]}]},
    "matrix": {"x": "esfuerzo", "y": "impacto", "quadrants": ["ya", "planificar", "si sobra", "descartar"],
               "items": [{"label": "uno", "x": 0.25, "y": 0.8}, {"label": "dos", "x": 0.8, "y": 0.75}, {"label": "tres", "x": 0.7, "y": 0.2}]},
    "helix": {"labels": ["hebra A", "hebra B"], "items": ["inicio", "medio", "fin"]},
    "wave": {"label": "señal"},
    "radar": {"labels": ["precio", "calidad", "rapidez", "soporte", "diseño"],
              "series": [{"name": "nosotros", "values": [4, 5, 3, 4, 5]}, {"name": "rival", "values": [5, 3, 4, 2, 3]}]},
    "line": {"labels": ["T1", "T2", "T3", "T4"], "series": [{"name": "ventas", "values": [2, 3, 2.5, 5]}]},
    "venn": {"items": ["producto", "mercado"], "center": "encaje"},
    "domino": {"items": ["causa", "paso 1", "paso 2", "paso 3", "efecto"]},
    "puzzle": {"items": ["datos", "equipo", "proceso", "cliente"], "label": "todo encaja"},
    "shield": {"label": "sistema", "threats": ["phishing", "malware"], "unit": "bloqueados"},
    "rocket": {"items": [{"label": "beta", "sub": "T1"}, {"label": "lanzamiento", "sub": "T2"}, {"label": "100 clientes", "sub": "T4"}]},
    "globe": {"items": ["Madrid", "Lima", "Tokio", "Lagos", "Sídney"]},
    "scatter": {"items": ["jóvenes", "familias", "empresas"]},
    "layers": {"items": [{"label": "interfaz", "sub": "web y móvil"}, {"label": "lógica", "sub": "servicios"}, {"label": "datos", "sub": "almacén"}]},
    "morph": {"label": "transformación"},
}

DEFAULT_THEME = {"ink": "#0d1012", "ink2": "#14181b", "rule": "#2b3237", "bone": "#ece6d4",
                 "dim": "#8c9399", "hot": "#ff5a1f", "ok": "#a3b565"}
TEXTS = {
    "es": {"hint": "<kbd>←</kbd><kbd>→</kbd> navegar <kbd>O</kbd> índice <kbd>P</kbd> auto <kbd>F</kbd> pantalla completa",
           "overview": "Vista general · pulsa O o Esc para cerrar",
           "err": "No se pudo cargar three.min.js. Deja ese archivo junto a este HTML."},
    "en": {"hint": "<kbd>←</kbd><kbd>→</kbd> navigate <kbd>O</kbd> overview <kbd>P</kbd> auto <kbd>F</kbd> fullscreen",
           "overview": "Overview · press O or Esc to close",
           "err": "Could not load three.min.js. Keep that file next to this HTML."},
}


def say(msg):
    """Imprime sin romperse en consolas que no son UTF-8 (cp1252 en Windows)."""
    enc = sys.stdout.encoding or "utf-8"
    print(msg.encode(enc, "replace").decode(enc))


def warn(msg):
    enc = sys.stderr.encoding or "utf-8"
    print(("AVISO: " + msg).encode(enc, "replace").decode(enc), file=sys.stderr)


def slide_html(s, i):
    """Un <section> por diapositiva. Los textos admiten <em>, <b> y <br>."""
    hero = s.get("hero", i == 0)
    side = " right" if s.get("side") == "right" else ""
    p = [f'<section class="slide{side}">', '  <div class="col rv">']
    if not hero:
        p.append('    <div class="no">00</div>')
    if s.get("kicker"):
        p.append(f'    <div class="kick">{s["kicker"]}</div>')
    tag = "h1" if hero else "h2"
    p.append(f'    <{tag}>{s.get("title", "")}</{tag}>')
    if s.get("text"):
        p.append(f'    <p>{s["text"]}</p>')
    if s.get("rows"):
        p.append("    <dl>")
        for dt, dd in s["rows"]:
            p.append(f"      <div><dt>{dt}</dt><dd>{dd}</dd></div>")
        p.append("    </dl>")
    if s.get("stats"):
        p.append('    <div class="stats">')
        for st in s["stats"]:
            tone = f' {st["tone"]}' if st.get("tone") in ("ok", "hot") else ""
            suf = st.get("suffix", "")
            p.append(f'      <div><div class="v{tone}"><span class="cu" data-to="{st["value"]}" '
                     f'data-dec="{st.get("dec", 0)}">0</span>{suf}</div><div class="k">{st.get("label", "")}</div></div>')
        p.append("    </div>")
    if s.get("note"):
        p.append(f'    <p class="note">{s["note"]}</p>')
    p.append("  </div>")
    if s.get("notes"):
        p.append(f'  <div class="sn">{s["notes"]}</div>')
    p.append("</section>")
    return "\n".join(p)


def labels_of(data):
    """Textos que acaban como etiqueta 3D, para avisar si son largos."""
    out = []
    for key in ("items", "labels", "outputs", "layerNames", "quadrants", "threats"):
        for x in data.get(key) or []:
            if isinstance(x, str):
                out.append(x)
            elif isinstance(x, dict):
                out.append(str(x.get("label", "")))
                out += [c if isinstance(c, str) else str(c.get("label", "")) for c in x.get("children") or []]
    return out


def check(spec, slides):
    """Errores que impiden construir (sys.exit) y avisos de calidad (stderr)."""
    for key, obj, where in [("intro", spec, "spec")] + [("intro", s, f"slide {i + 1}") for i, s in enumerate(slides)]:
        if obj.get(key) and obj[key] not in INTROS:
            sys.exit(f"{where}: intro desconocida '{obj[key]}'. Válidas: {sorted(INTROS)}")
    for i, s in enumerate(slides):
        n, sc, data = i + 1, s.get("scene"), s.get("data") or {}
        if sc and sc not in SCENES:
            sys.exit(f"Slide {n}: escena desconocida '{sc}'. Válidas: {sorted(SCENES)}")
        if not sc:
            warn(f"slide {n}: sin 'scene'; el motor asignará una genérica")
        if not s.get("title"):
            warn(f"slide {n}: sin título")
        limit = SCENES[sc][1] if sc else None
        items = data.get("items") or []
        if limit and len(items) > limit:
            warn(f"slide {n} ({sc}): {len(items)} items; se leen bien hasta {limit} (el resto se recorta o se amontona)")
        long = [t for t in labels_of(data) if len(t) > LABEL_MAX]
        if long:
            warn(f"slide {n} ({sc}): etiquetas 3D largas (> {LABEL_MAX} caracteres): {', '.join(long[:4])}")
        if sc in WIDE and s.get("side") == "right":
            warn(f"slide {n} ({sc}): escena ancha con side:right; puede pisar el texto")
        if len(s.get("rows") or []) > 5:
            warn(f"slide {n}: más de 5 filas en 'rows'")
        if len(s.get("stats") or []) > 3:
            warn(f"slide {n}: más de 3 'stats'")
    if len(slides) > 16:
        warn(f"{len(slides)} diapositivas; por encima de 12-14 la presentación se hace larga")
    used = [s.get("scene") for s in slides if s.get("scene")]
    for sc in sorted(set(used)):
        if used.count(sc) > 2:
            warn(f"la escena '{sc}' se usa {used.count(sc)} veces; hay {len(SCENES)} donde elegir")


def gallery_spec():
    slides = [{"scene": sc, "kicker": f"{i + 1:02d} / {len(SCENES)}", "title": f"<em>{sc}</em>", "text": desc,
               "data": SAMPLES.get(sc, {}), "hero": False}
              for i, (sc, (desc, _)) in enumerate(SCENES.items())]
    return {"title": "Galería de escenas", "hud": "presentacion-3d · galería", "intro": "auto", "autoSeconds": 8, "slides": slides}


def build(spec, out, single):
    slides = spec.get("slides") or sys.exit("El spec necesita una lista 'slides'.")
    check(spec, slides)
    lang = spec.get("lang", "es")
    txt = TEXTS.get(lang, TEXTS["es"])
    theme = {**DEFAULT_THEME, **spec.get("theme", {})}
    clean = {"theme": theme, "autoSeconds": spec.get("autoSeconds", 15), "intro": spec.get("intro", "none"),
             "slides": [{k: s[k] for k in ("scene", "data", "cam", "look", "intro") if k in s} for s in slides]}

    html = (ASSETS / "template.html").read_text(encoding="utf-8")
    rep = {"{{LANG}}": lang, "{{TITLE}}": spec.get("title", "Presentación"), "{{HUD}}": spec.get("hud", spec.get("title", "")),
           "{{HINT}}": txt["hint"], "{{OVERVIEW}}": txt["overview"], "{{ERR}}": txt["err"],
           "{{INK}}": theme["ink"], "{{INK2}}": theme["ink2"], "{{RULE}}": theme["rule"], "{{BONE}}": theme["bone"],
           "{{DIM}}": theme["dim"], "{{HOT}}": theme["hot"], "{{OK}}": theme["ok"],
           "{{SLIDES}}": "\n\n".join(slide_html(s, i) for i, s in enumerate(slides)),
           "{{SPEC_JSON}}": json.dumps(clean, ensure_ascii=False).replace("</", "<\\/")}
    for k, v in rep.items():
        html = html.replace(k, v)

    out.parent.mkdir(parents=True, exist_ok=True)
    if single:
        # se incrusta al final, ya sustituidos los marcadores, para que nada de three.js se confunda con uno
        three = (ASSETS / "three.min.js").read_text(encoding="utf-8").replace("</script", "<\\/script")
        tag = '<script src="three.min.js"></script>'
        if tag not in html:
            sys.exit("No encuentro la etiqueta de three.min.js en la plantilla; no puedo incrustarla.")
        html = html.replace(tag, "<script>\n" + three + "\n</script>")
    else:
        shutil.copy(ASSETS / "three.min.js", out.parent / "three.min.js")
    out.write_text(html, encoding="utf-8")
    say(f"OK - {len(slides)} diapositivas -> {out}" + (" (fichero único)" if single else " (+ three.min.js al lado)"))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    unknown = flags - {"--single", "--gallery", "--list"}
    if unknown:
        sys.exit(f"Opción desconocida: {' '.join(sorted(unknown))}\n{__doc__}")
    if "--list" in flags:
        for sc, (desc, limit) in SCENES.items():
            say(f"{sc:9s} {desc}" + (f"  (hasta {limit} items)" if limit else ""))
        return
    if "--gallery" in flags:
        if len(args) != 1:
            sys.exit(__doc__)
        return build(gallery_spec(), Path(args[0]), "--single" in flags)
    if len(args) != 2:
        sys.exit(__doc__)
    spec = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    build(spec, Path(args[1]), "--single" in flags)


if __name__ == "__main__":
    main()
