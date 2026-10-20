#!/usr/bin/env python3
"""Convierte cada notes/*.md en notes/*.html (con LaTeX vía KaTeX) y regenera index.html.
Requisitos: pandoc. Uso:  python3 build.py
"""
import re, subprocess
from pathlib import Path

ROOT = Path(__file__).parent
KATEX = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/"
CALLOUTS = {"Corregido": "fix", "Aclarado": "clar", "Añadido": "add", "Notación": "not"}

def title_of(md: Path) -> str:
    for line in md.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md.stem

def build_note(md: Path) -> str:
    html = md.with_suffix(".html")
    title = title_of(md)
    subprocess.run(["pandoc", str(md), "-f", "markdown", "-t", "html5", "-s",
                    f"--katex={KATEX}", "--toc", "--toc-depth=2",
                    "--css", "../style.css", "-V", "document-css=false", "-V", "lang=es",
                    "--metadata", f"pagetitle={title}", "-o", str(html)], check=True)
    text = html.read_text(encoding="utf-8")
    for label, cls in CALLOUTS.items():
        text = re.sub(rf'<blockquote>(\s*<p><strong>\[{label})', rf'<blockquote class="{cls}">\1', text)
    text = re.sub(r'<h2 id="(hoja-resumen[^"]*)"', r'<h2 id="\1" class="pagebreak"', text)
    html.write_text(text, encoding="utf-8")
    return title

notes = sorted((ROOT / "notes").glob("*.md"))
items = [(n.with_suffix(".html").name, build_note(n)) for n in notes]

links = "\n".join(
    f'    <li><a href="notes/{h}">{t}</a> <small>(<a href="notes/{h[:-5]}.md">fuente .md</a>)</small></li>'
    for h, t in items)
(ROOT / "index.html").write_text(f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cuaderno de Física 3</title><link rel="stylesheet" href="style.css"></head>
<body><h1>Cuaderno de Física 3</h1>
<p><em>Electrodinámica · notas propias, versionadas en el repositorio.</em></p>
<h2>Notas</h2>
<ul>
{links}
</ul>
</body></html>
""", encoding="utf-8")
print("Generado:", ", ".join(h for h, _ in items), "+ index.html")

# Verificación: todos los enlaces locales de index.html y de las notas deben existir
broken = []
for page in [ROOT / "index.html", *(ROOT / "notes").glob("*.html")]:
    for href in re.findall(r'(?:href|src)="([^"#:]+)"', page.read_text(encoding="utf-8")):
        if not (page.parent / href).exists():
            broken.append(f"{page.name} -> {href}")
print("Enlaces rotos:" if broken else "Enlaces verificados: OK", *broken, sep="\n  " if broken else " ")
