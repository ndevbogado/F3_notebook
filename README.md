# Cuaderno de Física 3

Notas propias de electrodinámica, escritas en Markdown con LaTeX y convertidas a HTML.

## Estructura

```
index.html                 página de inicio (lista de notas), se genera sola
style.css                  estilo compartido (modo claro/oscuro, impresión)
build.py                   convierte notes/*.md -> notes/*.html y regenera index.html
notes/                     una nota por sesión (.md es la fuente, .html se genera)
figures/                   imágenes; make_figures.py regenera los gráficos con Python
originals/                 tus PDFs manuscritos, sin tocar
reports/                   informe de cambios por cada nota transcripta
```

## Cómo agregar una nota nueva

1. Guardá el PDF manuscrito en `originals/`.
2. Escribí (o pedí que se escriba) `notes/02-nombre.md`.
3. Ejecutá `python3 build.py` (requiere [pandoc](https://pandoc.org)).
4. Hacé un commit con el `.md`, el `.html`, las figuras y el informe.

## Escribir fórmulas (LaTeX mínimo)

| Escribís | Se ve |
|---|---|
| `$\nabla f$` | gradiente de f |
| `$\nabla\cdot\mathbf{F}$` | divergencia de F |
| `$\nabla\times\mathbf{F}$` | rotor de F |
| `$\frac{\partial f}{\partial x}$` | derivada parcial |
| `$$ ... $$` | ecuación en su propia línea |

GitHub muestra las fórmulas de los `.md` directamente. Para ver el `.html` con fórmulas hace falta conexión a internet (KaTeX se carga desde cdnjs) y se abre con doble clic o con GitHub Pages.

## Recuadros de cambios

Cada cambio de Claude sobre tus notas va en un recuadro con etiqueta y código (`C` corregido o aclarado, `A` añadido, `N` notación) que coincide con el informe de `reports/`. Para aceptar un cambio, dejalo; para rechazarlo, borrá el recuadro.

## Figuras

- Gráficos calculables: se generan con `figures/make_figures.py` (Python + matplotlib).
- Dibujos a mano: guardá una foto o escaneo de al menos 1600 px de ancho en `figures/` y referenciala con `![descripción](../figures/archivo.png)`.
