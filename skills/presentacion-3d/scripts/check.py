#!/usr/bin/env python3
"""Comprueba una presentación en un navegador sin ventana y avisa de errores de JavaScript.

Uso:  python check.py salida/presentacion.html [--shots carpeta] [--slides 1,4,7]

Abre el fichero como file:// (igual que el doble clic del usuario) con ?selftest: el motor simula
30 s de animación de cada escena y escribe en la consola qué diapositivas fallan.
Con --shots guarda además una captura PNG de cada diapositiva (o de las de --slides), ya asentada.
Necesita Edge o Chrome instalados. Código de salida 1 si algo falla o no se puede confirmar.
"""
import re, shutil, subprocess, sys, tempfile
from pathlib import Path

CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]
NAMES = ["google-chrome", "chromium", "chromium-browser", "microsoft-edge", "msedge", "chrome"]
MSG = re.compile(r'CONSOLE[^"\n]*"([^\n]*?)", source: file:')  # solo mensajes de la página, no de extensiones


def browser():
    for c in CANDIDATES:
        if Path(c).exists():
            return c
    for n in NAMES:
        if shutil.which(n):
            return shutil.which(n)
    sys.exit("No encuentro Edge ni Chrome; no puedo comprobar la presentación. Ábrela a mano y mira la consola (F12).")


def run(exe, prof, url, extra):
    cmd = [exe, "--headless=new", f"--user-data-dir={prof}", "--enable-logging=stderr", "--v=0",
           "--window-size=1280,720", "--virtual-time-budget=5000", "--hide-scrollbars"] + extra + [url]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
        return MSG.findall(r.stderr or "")
    except subprocess.TimeoutExpired:
        return ["Uncaught: el navegador no terminó en 180 s"]


def main():
    args = sys.argv[1:]
    shots = only = None
    if "--shots" in args:
        i = args.index("--shots"); shots = Path(args[i + 1]); del args[i:i + 2]
    if "--slides" in args:
        i = args.index("--slides"); only = [int(x) for x in args[i + 1].split(",")]; del args[i:i + 2]
    if len(args) != 1:
        sys.exit(__doc__)
    html = Path(args[0]).resolve()
    if not html.exists():
        sys.exit(f"No existe {html}")
    total = len(re.findall(r'<section class="slide', html.read_text(encoding="utf-8")))
    exe = browser()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as prof:
        msgs = run(exe, prof, html.as_uri() + "?selftest", ["--dump-dom"])
        errors = [m for m in msgs if "Uncaught" in m or ("[presentacion-3d]" in m and "selftest:" not in m)]
        summary = [m for m in msgs if "selftest:" in m]
        for m in errors:
            print("ERROR  " + m.replace("\\n", " ")[:400])
        if shots:
            shots.mkdir(parents=True, exist_ok=True)
            for n in only or range(1, total + 1):
                shot = (shots / f"slide-{n:02d}.png").resolve()
                errors += [m for m in run(exe, prof, f"{html.as_uri()}?shot#{n}", [f"--screenshot={shot}"]) if "Uncaught" in m]
            print(f"capturas en {shots}")
    if not summary:
        print("No he podido confirmar el resultado: el motor no escribió el resumen del selftest (¿falló al arrancar?)")
        sys.exit(1)
    print(f"{total} diapositivas - " + summary[0].split("selftest:")[1].strip() + (f" - {len(errors)} errores" if errors else ""))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
