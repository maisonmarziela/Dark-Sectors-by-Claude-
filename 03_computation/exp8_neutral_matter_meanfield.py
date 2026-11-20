"""Experiment 8 - does photon kinetic mixing give neutral matter a mean-field energy inside neutral matter?

With kinetic mixing epsilon, a sector-B charge q' looks to sector A like an ordinary charge
epsilon*q'.  The first-order (frozen-density) interaction energy between an ordinary atom and a
"mirror" atom at separation R is therefore epsilon times the classical electrostatic energy V(R)
of two neutral charge distributions.  For a B body interpenetrating an A body with uncorrelated
atomic positions the mean energy per pair is   n * int V(R) d^3R.

Claim (manuscript Lemma 2): for neutral atoms   int V(R) d^3R = 0   exactly, because the
Fourier transform obeys  V~(q) = 4 pi rho~_1(q) rho~_2(q)/q^2  and  rho~(q) = O(q^2) for a
neutral distribution.  The short-distance nucleus-nucleus repulsion is cancelled by the
attraction between each nucleus and the other atom's electron cloud.

This script checks the cancellation by direct real-space quadrature for model atoms (point
nucleus + exponential electron cloud of radius b), verifies the real-space V(R) against an
independent Fourier-space evaluation, and reports how large each of the two cancelling pieces is.
One of the two pieces, kept alone, has the same form (2 pi Z Z' e^2 epsilon r_2^2 per unit
number density) as a published estimate of a nonzero mean energy of mirror atoms embedded in
ordinary matter (Mitra & Foot 2003, appendix).  Whether that estimate really omits the
compensating piece is OUR reading of the paper and needs independent verification by someone
other than us - see the manuscript, Sec. 5.3, for the careful statement.

Units: e^2/(4 pi eps0) = 1, lengths in units of the Bohr radius; V in Hartree * (Z1 Z2 epsilon).
"""
from __future__ import annotations

import numpy as np
from scipy import integrate

from crh_common import BLUE, INK2, ORANGE, save_json, setup_matplotlib


def phi_atom(r, b):
    """Electrostatic potential of a unit point nucleus plus a unit exponential cloud n = exp(-2r/b)/(pi b^3)."""
    return (1.0 / r + 1.0 / b) * np.exp(-2.0 * r / b)


def cloud(r, b):
    return np.exp(-2.0 * r / b) / (np.pi * b**3)


def V_real(R, b1, b2):
    """Interaction energy of two unit neutral atoms at separation R (real-space quadrature)."""
    # V = phi_1(R) - (n_2 * phi_1)(R);  convolution of radial functions:
    # (n_2*phi_1)(R) = (2 pi / R) int_0^inf y n_2(y) [ G(R+y) - G(|R-y|) ] dy,  G(s) = int^s s' phi_1(s') ds'
    G = lambda s: -np.exp(-2.0 * s / b1) * (0.75 * b1 + 0.5 * s)
    f = lambda y: y * cloud(y, b2) * (G(R + y) - G(abs(R - y)))
    kw = dict(limit=400, epsabs=1e-15, epsrel=1e-12)
    conv = 2 * np.pi / R * (integrate.quad(f, 0, R, **kw)[0] + integrate.quad(f, R, np.inf, **kw)[0])
    return phi_atom(R, b1) - conv


def V_fourier(R, b1, b2):
    """Same quantity from V~(q) = 4 pi (1-F1)(1-F2)/q^2 with F = (1+q^2 b^2/4)^-2."""
    F = lambda q, b: (1 + q * q * b * b / 4) ** -2
    g = lambda q: (1 - F(q, b1)) * (1 - F(q, b2)) * np.sinc(q * R / np.pi)      # sin(qR)/(qR)
    val = integrate.quad(g, 0, 400.0, limit=4000, epsabs=1e-13, epsrel=1e-11)[0]
    # tail beyond q=400: integrand -> sin(qR)/(qR), integral = (pi/2 - Si(400 R)) / R
    from scipy.special import sici
    tail = (np.pi / 2 - sici(400.0 * R)[0]) / R
    return 2 / np.pi * (val + tail)


def main() -> int:
    plt = setup_matplotlib()
    out = {"cases": []}
    print("volume integral of the atom-atom electrostatic energy, int V d^3R  (should vanish)")
    for b1, b2 in ((1.0, 1.0), (1.0, 0.25), (1.0, 0.05), (0.6, 1.7)):
        Rg = np.geomspace(1e-4, 60.0 * max(b1, b2), 1400)
        V = np.array([V_real(R, b1, b2) for R in Rg])
        w = 4 * np.pi * Rg**2 * V
        total = np.trapezoid(w, Rg) + 2 * np.pi * Rg[0] ** 2            # analytic 1/R core below the first grid point
        pos = np.trapezoid(np.clip(w, 0, None), Rg) + 2 * np.pi * Rg[0] ** 2
        neg = np.trapezoid(np.clip(w, None, 0), Rg)
        # the two physically distinct pieces:
        #   nucleus_1 in the full potential of atom 2 ............ + 2 pi b2^2
        #   electron cloud_1 in the full potential of atom 2 ..... - 2 pi b2^2
        piece = 2 * np.pi * min(b1, b2) ** 2
        # independent check of V(R) itself
        chk = max(abs(V_real(R, b1, b2) - V_fourier(R, b1, b2)) / abs(V_real(R, b1, b2)) for R in (0.3, 1.0, 2.5))
        print(f"   b1={b1:4.2f} b2={b2:4.2f}:  positive part = {pos:+.6f}   negative part = {neg:+.6f}"
              f"   total = {total:+.2e}   |total|/positive = {abs(total) / pos:.1e}   real-vs-Fourier V: {chk:.1e}")
        out["cases"].append({"b1": b1, "b2": b2, "positive_part": pos, "negative_part": neg, "total": total,
                             "relative_residual": abs(total) / pos, "nucleus_only_piece_2pi_b2": piece,
                             "V_check_rel_err": chk})
    worst = max(c["relative_residual"] for c in out["cases"])

    # how large is the piece one gets by keeping ONLY "nucleus in the screened field of the other atom"?
    a0_cm, Eh_eV = 0.529e-8, 27.211
    Z, Zp, n_atoms = 8, 8, 1.0 / (4 / 3 * np.pi * (3e-8) ** 3)        # atoms per cm^3 for mean spacing a = 3e-8 cm
    r2 = 4.0 / Zp                                                    # screening length 4 a0 / Z' (in a0)
    kept = n_atoms * a0_cm**3 * 2 * np.pi * r2**2 * Z * Zp * Eh_eV    # eV per unit epsilon
    print(f"keeping only the nucleus-nucleus piece (Z = Z' = 8, r2 = 4a0/Z', a = 3e-8 cm) would give"
          f" <zeta> ~ epsilon x {kept:.0f} eV;  with the electron-cloud piece included the sum is zero.")
    out["nucleus_only_estimate_eV_per_epsilon"] = kept

    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    R = np.geomspace(0.05, 12, 500)
    V = np.array([V_real(r, 1.0, 1.0) for r in R])
    ax.plot(R, 4 * np.pi * R**2 * V, color=BLUE)
    ax.fill_between(R, 4 * np.pi * R**2 * V, 0, where=V > 0, color=BLUE, alpha=0.18, lw=0)
    ax.fill_between(R, 4 * np.pi * R**2 * V, 0, where=V < 0, color=ORANGE, alpha=0.25, lw=0)
    ax.axhline(0, color=INK2, lw=0.7)
    ax.text(1.55, 1.75, "nuclei close:\nrepulsion", color=INK2, fontsize=9)
    ax.text(4.5, -0.98, "nucleus inside the other\natom's electron cloud:\nattraction", color=INK2, fontsize=9)
    ax.set_xlabel("separation R  [Bohr radii]"); ax.set_ylabel("$4\\pi R^2\\,V(R)$   [arb. units]")
    ax.set_title("Neutral atom on neutral atom: the two areas cancel exactly")
    fig.savefig("results/exp8_neutral_matter_meanfield.png")
    plt.close(fig)

    out["worst_relative_residual"] = worst
    save_json("exp8_neutral_matter_meanfield.json", out)
    ok = worst < 1e-4
    print("RESULT:", f"mean-field energy cancels to {worst:.1e} of either piece" if ok else "CANCELLATION NOT CONFIRMED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
