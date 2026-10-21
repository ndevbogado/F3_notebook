# CONTEXT.md: briefing para continuar este proyecto con Claude

> **Cómo usarlo:** al empezar una conversación nueva, subí este archivo junto con tu PDF y escribí algo como:
> *"Lee CONTEXT.md y procesá este PDF como la próxima nota."*
> Si cambiás una regla del proyecto, editá este archivo (es la única fuente de verdad).

## 1. Qué es el proyecto

Cuaderno web personal de **Física 3 (electrodinámica, UBA)**. La persona escribe apuntes a mano (PDF/foto, en español) y Claude los convierte en notas formales en **Markdown + LaTeX**, que luego se compilan a **HTML**. Todo se versiona en un repositorio git.

Contexto de estudio: estudia con Griffiths (*Introduction to Electrodynamics*), Feynman II y Purcell & Morin. Examen 23/11/2026 (Guías 4 a 6: magnetismo y circuitos AC) y 30/11/2026 (Guías 1 a 3: campo eléctrico y circuitos DC). Las notas se numeran por sesión de estudio (`01-…`, `02-…`).

## 2. Flujo de trabajo (obligatorio)

1. La persona sube `nota.pdf` (se copia a `originals/` sin tocar).
2. Claude lee la escritura a mano, transcribe y **ordena/mejora** el contenido, y escribe `notes/NN-nombre.md`.
3. Claude escribe el informe `reports/NN-nombre-changes.txt` (ver sección 5).
4. `python3 build.py` genera `notes/NN-nombre.html`, `index.html`, la copia autocontenida en `single/` y verifica los enlaces.
5. Claude entrega un `.zip` actualizado del repositorio y el informe `.txt` aparte.

**Claude hace la transcripción** (build.py no lee manuscritos). Si la persona edita el `.md` a mano, solo tiene que volver a correr `python3 build.py`.

## 3. Estructura del repositorio

```
index.html            índice (generado; lista cada nota + enlace al .md fuente)
style.css             estilo compartido (claro/oscuro, impresión, recuadros, navegación)
build.py              pandoc: notes/*.md -> notes/*.html; navegación; index; single/; chequeo de enlaces
serve.sh              servidor local en http://localhost:8000
CONTEXT.md            este archivo
README.md             guía de uso para la persona
notes/                NN-nombre.md (fuente) + .html (generado)
figures/              imágenes + make_figures.py (gráficos con matplotlib)
originals/            PDFs manuscritos originales (nunca se modifican)
reports/              NN-nombre-changes.txt
single/               copias autocontenidas (CSS e imágenes incrustados); ignorada por git
```

Requisitos: `pandoc`, `python3` (+ matplotlib para las figuras). Las ecuaciones usan KaTeX desde cdnjs (versión 0.16.9), así que el HTML necesita internet para mostrarlas.

## 4. Convenciones de contenido

- **Idioma:** cuaderno en **español** (rioplatense, voseo en instrucciones al lector); informe `.txt` en **inglés**.
- **Notación:** campo escalar $f,g$; campo vectorial $\mathbf{F},\mathbf{A}$ (negrita); versores $\hat{x},\hat{y},\hat{z}$. Si los apuntes mezclan símbolos, se unifica y se registra como `N`.
- **Estructura de cada nota:** título `#`, párrafo de fuente y leyenda de recuadros, secciones `## N. …` numeradas a mano, "Pendientes" al final y **hoja resumen de 1 página como última sección** (el HTML la imprime en página aparte; `build.py` detecta el `id` que empieza con `hoja-resumen`).
- **Ecuaciones:** `$…$` en línea y `$$…$$` en bloque. En celdas de tablas Markdown **no usar el carácter `|`**: usar `\lvert … \rvert`.
- **Recuadros de cambios** (blockquote cuyo primer texto es una etiqueta en negrita; `build.py` los colorea por la palabra inicial):
  - `> **[Corregido · C#]** …` error de los apuntes (decir qué decía y cómo queda)
  - `> **[Aclarado · C#]** …` frase ambigua reformulada
  - `> **[Añadido por Claude · A#]** …` contenido nuevo
  - `> **[Notación · N#]** …` unificación de símbolos
  - Los códigos coinciden con el informe. Todo cambio o agregado debe tener recuadro.
- **Reglas de rigor:** no inventar contenido; marcar lo ilegible como `[ilegible]` y dejarlo en el informe; verificar identidades con SymPy antes de afirmarlas; si algo es incierto, decirlo.
- **Instrucciones dentro de los apuntes** (p. ej. "[CLAUDE busca…]"): se ejecutan y la línea **no** se copia al cuaderno; se registran en el informe como `I#`.
- **Figuras:** lo calculable se grafica con `figures/make_figures.py` (paleta: tinta `#1f2a44`, acento `#c2410c`, fondo de grilla `#d5dbe6`); los dibujos a mano se reciben como foto/escaneo (≥1600 px), se recortan y se incrustan con epígrafe.

## 5. Formato del informe de cambios (`reports/NN-nombre-changes.txt`)

Encabezado (fuente, resultado, fecha, idioma) y secciones: `0. Illegible parts`, `1. Notation (N)`, `2. Reorganization (R)`, `3. Corrections and clarifications (C)`, lo verificado que quedó sin cambios, `4. Additions by Claude (A)`, `5. Instructions found in the notes (I)`, `6. Build and technical notes`. Cada entrada: **ID, dónde (página/sección), qué decían los apuntes, qué queda, por qué**.

## 6. Diseño

Hoja cuadriculada sutil (como el cuaderno físico), tipografía serif (Source Serif 4 con respaldo Georgia), ancho de lectura ~46rem, modo claro/oscuro automático, colores de recuadros: corregido ámbar, aclarado verde azulado, añadido azul, notación violeta. Barra de navegación (Anterior · Índice · Siguiente) arriba y abajo de cada nota; se oculta al imprimir y no existe en `single/`. Accesibilidad: foco visible, sin depender solo del color (cada recuadro tiene etiqueta de texto).

## 7. Problemas conocidos

- **Firefox en Flatpak (SteamOS):** al abrir un `.html` con el selector de archivos, la dirección es `file:///run/user/…/doc/…` y el navegador solo ve ese archivo (se rompen CSS, imágenes y enlaces). Soluciones: `./serve.sh` (recomendada), abrir `single/NOMBRE.html`, o dar permiso con `flatpak override`. No usar rutas `file:///run/user/…` en los enlaces.
- GitHub no muestra el `.html` como página (sí renderiza el `.md` con LaTeX); para verlo hace falta GitHub Pages.
- No se puede probar el renderizado de KaTeX en el entorno de Claude (sin navegador ni internet): si una fórmula se ve mal, avisar cuál.

## 8. Estado actual

- Hecha: `01-math-toolkit` (gradiente, divergencia, rotor, productos, operadores de segundo orden, hoja resumen).
- Pendiente de la sesión 1: teoremas de la divergencia y de Stokes (B), coordenadas esféricas y cilíndricas (C), delta de Dirac (D). Se agregarán como `02-….md` cuando la persona los suba.
- Ideas a futuro: GitHub Actions para compilar y publicar el HTML al subir un `.md`; script con la API de Claude que deje borradores en una carpeta de revisión (nunca publicar sin que la persona revise).
