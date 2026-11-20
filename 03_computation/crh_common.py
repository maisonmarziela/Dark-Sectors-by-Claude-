"""Shared helpers for the Project CRH computational experiments.

Everything here is deliberately small and dependency-light (numpy, scipy,
matplotlib only) so the experiments can be re-run anywhere.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

RESULTS = Path(__file__).resolve().parent / "results"
RESULTS.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------
# Plot style.  Colours are the first slots of a categorical palette that was
# checked with a colour-vision-deficiency validator (adjacent and all-pairs
# separation pass for slots 1-3).  Identity is never carried by colour alone:
# every multi-series figure has a legend and distinct line styles/markers, and
# every figure's numbers are also written to a JSON table in results/.
# ----------------------------------------------------------------------------
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"


def setup_matplotlib():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "font.family": "sans-serif", "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
        "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.edgecolor": AXIS, "axes.linewidth": 0.8, "axes.labelcolor": INK2,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "grid.linestyle": "-",
        "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
        "text.color": INK, "legend.frameon": False, "legend.fontsize": 9,
        "lines.linewidth": 2.0, "lines.markersize": 7, "figure.dpi": 110, "savefig.dpi": 160,
        "savefig.bbox": "tight", "axes.axisbelow": True,
    })
    return plt


def save_json(name: str, obj) -> Path:
    """Write a results table (the 'table view' of every figure)."""

    def default(o):
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (np.bool_,)):
            return bool(o)
        raise TypeError(type(o))

    path = RESULTS / name
    path.write_text(json.dumps(obj, indent=2, default=default), encoding="utf-8")
    return path


class Timer:
    def __init__(self, label: str):
        self.label = label

    def __enter__(self):
        self.t0 = time.perf_counter()
        return self

    def __exit__(self, *exc):
        print(f"[{self.label}] {time.perf_counter() - self.t0:.1f} s")


# ----------------------------------------------------------------------------
# 1+1D lattice field helpers (periodic box, second-order centred differences).
# ----------------------------------------------------------------------------
def lap(f: np.ndarray, dx: float) -> np.ndarray:
    """Periodic second-order Laplacian."""
    return (np.roll(f, -1) - 2.0 * f + np.roll(f, 1)) / dx**2


def grad_c(f: np.ndarray, dx: float) -> np.ndarray:
    """Periodic centred first derivative."""
    return (np.roll(f, -1) - np.roll(f, 1)) / (2.0 * dx)


def field_energy(phi: np.ndarray, pi: np.ndarray, m2: float, dx: float) -> float:
    """Discrete energy of a free massive field: sum of 1/2 pi^2 + 1/2 (d phi)^2 + 1/2 m^2 phi^2.

    The gradient term uses the forward difference, which is the form whose
    variation gives exactly the centred Laplacian used in the equations of
    motion (so the semi-discrete system is exactly Hamiltonian)."""
    d = (np.roll(phi, -1) - phi) / dx
    return float(dx * np.sum(0.5 * pi**2 + 0.5 * d**2 + 0.5 * m2 * phi**2))


def field_momentum(phi: np.ndarray, pi: np.ndarray, dx: float) -> float:
    """Discrete field momentum  P = -int pi d_x phi dx  (centred difference)."""
    return float(-dx * np.sum(pi * grad_c(phi, dx)))


def smooth_noise(rng: np.random.Generator, n: int, dx: float, amp: float, kmax: float) -> np.ndarray:
    """Band-limited real Gaussian noise with rms amplitude `amp` and wavenumbers |k| < kmax.

    Used as a *classical proxy* for the fluctuations (quantum or thermal) that
    seed a symmetry-breaking instability.  It is not a model of the quantum state."""
    k = 2.0 * np.pi * np.fft.rfftfreq(n, d=dx)
    spec = (rng.normal(size=k.size) + 1j * rng.normal(size=k.size)) * (np.abs(k) < kmax)
    spec[0] = 0.0
    f = np.fft.irfft(spec, n=n)
    rms = np.sqrt(np.mean(f**2))
    return f * (amp / rms) if rms > 0 else f
