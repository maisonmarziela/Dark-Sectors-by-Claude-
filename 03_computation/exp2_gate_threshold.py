"""Experiment 2 - when does an overlap-triggered gate open?  (linear stability of chi = 0)

For the even ("threshold") gate the closed state chi = 0 is stable iff the operator

        H = -Laplacian + mu^2 [ 1 - r(x) ],       r(x) = g O_A(x) O_B(x) / mu^2   ("overlap ratio")

has no negative eigenvalue (Theorem 2 of the manuscript).  For a uniform overlap
of ratio r > 1 the analytic finite-size thresholds are

    slab of width L (1D):   L_c(r) = 2 arctan(1/sqrt(r-1)) / (mu sqrt(r-1))
    ball of radius R (3D):  R_c(r) = (pi - arctan sqrt(r-1)) / (mu sqrt(r-1))

This script (i) finds the thresholds numerically with a finite-difference
eigenvalue solver that knows nothing about those formulas, (ii) checks
second-order convergence, (iii) checks the Sobolev-inequality sufficient
condition for isolation, and (iv) computes the threshold for a smooth
(Gaussian) overlap, for which no closed form is used.

Units: mu = 1.
"""
from __future__ import annotations

import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

from crh_common import BLUE, INK2, ORANGE, Timer, save_json, setup_matplotlib

SOBOLEV_3D = 3.0 * (np.pi / 2.0) ** (4.0 / 3.0)   # sharp constant: |grad u|_2^2 >= S |u|_6^2 in R^3


def Lc_slab(r):
    s = np.sqrt(r - 1.0)
    return 2.0 * np.arctan(1.0 / s) / s


def Rc_ball(r):
    s = np.sqrt(r - 1.0)
    return (np.pi - np.arctan(s)) / s


def lowest_eig_1d(rfun, half_width: float, h: float) -> float:
    """Lowest eigenvalue of -d^2/dx^2 + 1 - r(x) on [-X, X] (Dirichlet), cell-centred grid."""
    n = int(round(2 * half_width / h))
    x = -half_width + (np.arange(n) + 0.5) * h
    d = 2.0 / h**2 + 1.0 - rfun(x)
    e = -np.ones(n - 1) / h**2
    return float(eigh_tridiagonal(d, e, select="i", select_range=(0, 0), eigvals_only=True)[0])


def lowest_eig_radial(rfun, rho_max: float, h: float) -> float:
    """Lowest s-wave eigenvalue of -Laplacian + 1 - r(rho) in 3D, via u = rho*chi, u(0)=0.

    Grid rho_j = j h (j = 1..n), so u(0) = 0 is imposed exactly; the profile is sampled at nodes."""
    n = int(round(rho_max / h)) - 1
    rho = (np.arange(n) + 1.0) * h
    d = 2.0 / h**2 + 1.0 - rfun(rho)
    e = -np.ones(n - 1) / h**2
    return float(eigh_tridiagonal(d, e, select="i", select_range=(0, 0), eigvals_only=True)[0])


def slab_profile(r, L):
    return lambda x: np.where(np.abs(x) < L / 2, r, 0.0)


def ball_profile(r, R, h):
    # sharp ball sampled at nodes; a node exactly on the surface gets half weight (trapezoid rule)
    def f(rho):
        return np.where(rho < R - 1e-12, r, np.where(np.abs(rho - R) <= 1e-12, 0.5 * r, 0.0))
    return f


def numeric_rc_slab(L, h, pad=18.0):
    g = lambda r: lowest_eig_1d(slab_profile(r, L), L / 2 + pad, h)
    return brentq(g, 1.0 + 1e-9, 400.0, xtol=1e-12)


def numeric_rc_ball(R, h, pad=18.0):
    g = lambda r: lowest_eig_radial(ball_profile(r, R, h), R + pad, h)
    return brentq(g, 1.0 + 1e-9, 400.0, xtol=1e-12)


def main() -> int:
    plt = setup_matplotlib()
    out: dict = {"sobolev_constant_3d": SOBOLEV_3D}

    # ---------------------------------------------------------------- slab & ball thresholds
    print("threshold overlap ratio r_c for a given size: numeric vs analytic")
    Ls = np.array([0.25, 0.5, 1.0, 2.0, 4.0, 8.0])
    Rs = np.array([1.0, 1.5, 2.0, 3.0, 5.0, 8.0])
    h = 0.005
    rows_slab, rows_ball = [], []
    with Timer("thresholds"):
        for L in Ls:
            num = numeric_rc_slab(L, h)
            ana = brentq(lambda r: Lc_slab(r) - L, 1.0 + 1e-12, 1e6)
            rows_slab.append({"L": L, "r_c_numeric": num, "r_c_analytic": ana, "rel_err": abs(num - ana) / ana})
            print(f"   slab L={L:5.2f}: numeric r_c={num:10.6f}  analytic={ana:10.6f}  rel.err={abs(num-ana)/ana:.1e}")
        for R in Rs:
            num = numeric_rc_ball(R, h)
            ana = brentq(lambda r: Rc_ball(r) - R, 1.0 + 1e-12, 1e6)
            rows_ball.append({"R": R, "r_c_numeric": num, "r_c_analytic": ana, "rel_err": abs(num - ana) / ana})
            print(f"   ball R={R:5.2f}: numeric r_c={num:10.6f}  analytic={ana:10.6f}  rel.err={abs(num-ana)/ana:.1e}")
    out["slab"], out["ball"] = rows_slab, rows_ball

    # ---------------------------------------------------------------- convergence
    print("grid-convergence of the numeric threshold (slab L=2, ball R=2)")
    conv = []
    anaS = brentq(lambda r: Lc_slab(r) - 2.0, 1.0 + 1e-12, 1e6)
    anaB = brentq(lambda r: Rc_ball(r) - 2.0, 1.0 + 1e-12, 1e6)
    for hh in (0.04, 0.02, 0.01, 0.005):
        eS = abs(numeric_rc_slab(2.0, hh) - anaS)
        eB = abs(numeric_rc_ball(2.0, hh) - anaB)
        conv.append({"h": hh, "err_slab": eS, "err_ball": eB})
        print(f"   h={hh:6.3f}: |err| slab={eS:.3e}  ball={eB:.3e}")
    oS = [np.log2(conv[i]["err_slab"] / conv[i + 1]["err_slab"]) for i in range(len(conv) - 1)]
    oB = [np.log2(conv[i]["err_ball"] / conv[i + 1]["err_ball"]) for i in range(len(conv) - 1)]
    print(f"   observed order: slab {np.round(oS, 2)}, ball {np.round(oB, 2)}")
    out["convergence"] = {"rows": conv, "order_slab": oS, "order_ball": oB}

    # ---------------------------------------------------------------- Sobolev sufficient condition
    # Isolation is guaranteed if  || mu^2 (r-1)_+ ||_{L^{3/2}} <= S_3 .  For a uniform ball this reads
    # (r-1) (4 pi/3)^{2/3} R^2 <= S_3.  It must never contradict the exact threshold.
    print("Sobolev sufficient condition for isolation vs exact ball threshold")
    rr = np.geomspace(1.001, 1e4, 60)
    exact = (rr - 1.0) * Rc_ball(rr) ** 2 * (4 * np.pi / 3) ** (2 / 3)   # value of the L^{3/2} norm at threshold
    ok_sob = bool(np.all(exact >= SOBOLEV_3D))
    print(f"   min over r of ||U_+||_(3/2) at exact threshold = {exact.min():.4f}  >=  S_3 = {SOBOLEV_3D:.4f} : {ok_sob}")
    out["sobolev_check"] = {"min_norm_at_threshold": float(exact.min()), "S3": SOBOLEV_3D, "consistent": ok_sob}

    # ---------------------------------------------------------------- Gaussian overlap (no closed form used)
    print("Gaussian overlap r(rho) = r0 exp(-rho^2 / 2 sigma^2): numeric threshold r0_c(sigma)")
    gauss = []
    for sig in (0.5, 1.0, 2.0, 4.0, 8.0):
        g = lambda r0: lowest_eig_radial(lambda rho: r0 * np.exp(-rho**2 / (2 * sig**2)), 8 * sig + 20.0, 0.01)
        r0c = brentq(g, 1.0 + 1e-9, 5000.0, xtol=1e-10)
        # Sobolev norm of (r-1)_+ for this profile at threshold (numerical radial integral)
        rho = np.linspace(0, 8 * sig, 200001)
        up = np.clip(r0c * np.exp(-rho**2 / (2 * sig**2)) - 1.0, 0, None)
        norm = (np.trapezoid(4 * np.pi * rho**2 * up**1.5, rho)) ** (2 / 3)
        gauss.append({"sigma": sig, "r0_c": r0c, "L32_norm_at_threshold": float(norm), "exceeds_S3": bool(norm >= SOBOLEV_3D)})
        print(f"   sigma={sig:4.1f}: r0_c={r0c:9.4f}   ||U_+||_(3/2)={norm:7.3f}  (>= S_3: {norm >= SOBOLEV_3D})")
    out["gaussian_overlap"] = gauss

    # ---------------------------------------------------------------- figure: phase diagram
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    r = np.geomspace(1.02, 300, 400)
    ax.loglog(r - 1, Lc_slab(r), color=BLUE, label="slab width  $\\mu L_c$  (analytic)")
    ax.loglog(r - 1, Rc_ball(r), color=ORANGE, ls=(0, (6, 3)), label="ball radius  $\\mu R_c$  (analytic)")
    ax.loglog([q["r_c_numeric"] - 1 for q in rows_slab], Ls, "o", color=BLUE, mec="white", mew=1.5,
              label="slab, finite-difference eigen-solver")
    ax.loglog([q["r_c_numeric"] - 1 for q in rows_ball], Rs, "s", color=ORANGE, mec="white", mew=1.5,
              label="ball, finite-difference eigen-solver")
    ax.text(40, 6.5, "gate OPENS\n(closed state unstable)", color=INK2, fontsize=9, ha="center")
    ax.text(0.12, 0.5, "gate stays CLOSED\n(exact classical isolation)", color=INK2, fontsize=9, ha="center")
    ax.set_xlabel("overlap ratio above threshold,  $r-1 = g\\,O_AO_B/\\mu^2 - 1$")
    ax.set_ylabel("size of overlap region  [$1/\\mu$]")
    ax.set_title("Finite-size threshold of the overlap-triggered gate")
    ax.legend(loc="lower left")
    fig.savefig("results/exp2_gate_threshold.png")
    plt.close(fig)

    worst = max(max(q["rel_err"] for q in rows_slab), max(q["rel_err"] for q in rows_ball))
    out["worst_relative_error"] = worst
    save_json("exp2_gate_threshold.json", out)
    ok = worst < 2e-3 and ok_sob and all(q["exceeds_S3"] for q in gauss)
    print(f"RESULT: worst relative error numeric-vs-analytic = {worst:.1e};", "consistent" if ok else "CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
