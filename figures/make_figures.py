"""Regenera las figuras del cuaderno. Uso: python3 figures/make_figures.py"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).parent
INK, ACC, GRID = "#1f2a44", "#c2410c", "#d5dbe6"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": INK, "axes.labelcolor": INK,
                     "text.color": INK, "xtick.color": INK, "ytick.color": INK,
                     "mathtext.fontset": "cm", "figure.dpi": 150})

def clean(ax, lim=2.2):
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.grid(color=GRID, lw=.6)

# --- Figura 1: gradiente de un mínimo y de un punto silla
fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.4))
x = np.linspace(-2.2, 2.2, 400); X, Y = np.meshgrid(x, x)
xs = np.linspace(-2, 2, 7); XS, YS = np.meshgrid(xs, xs)
cases = [("$f = x^2 + y^2$  (mínimo)", lambda X, Y: X**2 + Y**2, lambda X, Y: (2*X, 2*Y)),
         ("$f = x^2 - y^2$  (punto silla)", lambda X, Y: X**2 - Y**2, lambda X, Y: (2*X, -2*Y))]
for ax, (title, f, g) in zip(axs, cases):
    ax.contour(X, Y, f(X, Y), levels=12, colors=INK, linewidths=.8, alpha=.55)
    U, V = g(XS, YS)
    ax.quiver(XS, YS, U, V, color=ACC, angles="xy", width=.008, pivot="mid", scale=70)
    ax.plot(0, 0, "o", color=INK, ms=7)
    ax.annotate(r"$\nabla f = 0$", (0, 0), (0.25, 0.35), color=INK, fontsize=11)
    ax.set_title(title); clean(ax)
fig.suptitle(r"Curvas de nivel (líneas finas) y gradiente $\nabla f$ (flechas)", y=1.0)
fig.tight_layout(); fig.savefig(OUT / "fig1_gradiente.png", bbox_inches="tight"); plt.close(fig)

# --- Figura 2: divergencia y rotor
fig, axs = plt.subplots(1, 3, figsize=(12, 4.2))
xs = np.linspace(-2, 2, 9); XS, YS = np.meshgrid(xs, xs)
fields = [(r"Fuente: $\mathbf{F}=(x,\,y)$" "\n" r"$\nabla\cdot\mathbf{F}=2>0$", XS, YS),
          (r"Sumidero: $\mathbf{F}=(-x,\,-y)$" "\n" r"$\nabla\cdot\mathbf{F}=-2<0$", -XS, -YS),
          (r"Giro: $\mathbf{F}=(-y,\,x)$" "\n" r"$\nabla\cdot\mathbf{F}=0,\ \ \nabla\times\mathbf{F}=2\,\hat{z}$", -YS, XS)]
for ax, (title, U, V) in zip(axs, fields):
    ax.quiver(XS, YS, U, V, color=ACC, angles="xy", width=.008, pivot="mid", scale=30)
    ax.plot(0, 0, "o", color=INK, ms=5); ax.set_title(title, fontsize=11); clean(ax)
fig.tight_layout(); fig.savefig(OUT / "fig2_divergencia_rotor.png", bbox_inches="tight"); plt.close(fig)
print("ok")
