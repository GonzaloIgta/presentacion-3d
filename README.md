# presentacion-3d

Skill para Claude Code que crea presentaciones web 3D animadas, para huir de las presentaciones de IA todas iguales (*AI slop*): cada diapositiva lleva una escena 3D viva que cuenta la idea, no un adorno junto al texto.

- Un único HTML que se abre con doble clic (Three.js, sin servidor).
- 33 escenas: red neuronal, dominó en cadena, capas, embudo, globo, engranajes, cohete, escudo…
- Algunas son interactivas (hover y clic).
- Teclado, índice, modo auto, notas del orador, pantalla completa y vista vertical en móvil.
- Das el tema y los apartados; la skill escribe el spec y construye el HTML.

**Demo (las 33 escenas):** https://claude.ai/artifact/LmEq9jjDHiHtve5dSrHk5s

## Instalar

```bash
npx skills add GonzaloIgta/presentacion-3d
```

o copia `skills/presentacion-3d` a `~/.claude/skills/`.

## Uso

Pide a Claude una presentación 3D sobre un tema. Necesita Python 3 para `scripts/build.py`; `scripts/check.py` usa Edge o Chrome si están instalados.

## Licencia

MIT. `assets/three.min.js` es Three.js (MIT, © Three.js Authors).
