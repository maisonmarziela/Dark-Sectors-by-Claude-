"""Experiment 3 - the open gate: static condensate, binding energy W, and the contact force.

For a fixed (static) overlap profile r(x) the gate field minimises

    E[chi] = int [ 1/2 |grad chi|^2 + 1/2 mu^2 (1 - r) chi^2 + 1/4 lambda chi^4 ] ,     W := -min E >= 0 .

Claims tested (manuscript Theorem 3 and Corollary):
  (i)   W = 0 below the finite-size threshold, W > 0 above it (continuous, second-order onset);
  (ii)  the rigorous bound  W <= int mu^4 (r-1)_+^2 / (4 lambda)  ("bulk bound");
  (iii) W is non-decreasing and convex in the overlap, so the force is ATTRACTIVE, and for a
        slab the force per unit area dW/dL tends to the bulk value u = mu^4 (r-1)^2/(4 lambda);
  (iv)  near threshold W matches the weakly-nonlinear prediction W = eps0^2 <psi^2>^2 / (4 lambda <psi^4>),
        an independent check that uses only the linear eigenproblem of Experiment 2.

Units: mu = 1.  Solver: Newton iteration on the discretised Euler-Lagrange equation
(tridiagonal Jacobian), seeded either from the bulk value or from the unstable eigenmode.
"""
from __future__ import annotations

import numpy as np
from scipy.linalg import eigh_tridiagonal, solve_banded

from crh_common import AQUA, BLUE, INK2, ORANGE, Timer, save_json, setup_matplotlib
from exp2_gate_threshold import Lc_slab, Rc_ball


def newton(chi, diag_lin, h, lam, weight=None, tol=1e-13, itmax=200):
    """Solve  -chi'' + diag_lin*chi + lam*w*chi^3 = 0  (Dirichlet), w = weight (1 for slab, 1/rho^2 radial)."""
    n = chi.size
    w = np.ones(n) if weight is None else weight
    off = -np.ones(n - 1) / h**2
    for _ in range(itmax):
        res = (2 * chi - np.r_[chi[1:], 0.0] - np.r_[0.0, chi[:-1]]) / h**2 + diag_lin * chi + lam * w * chi**3
        if np.max(np.abs(res)) < tol:
            break
        ab = np.zeros((3, n))
        ab[0, 1:] = off
        ab[1] = 2.0 / h**2 + diag_lin + 3 * lam * w * chi**2
        ab[2, :-1] = off
        step = solve_banded((1, 1), ab, -res)
        chi = chi + step
    return chi


def energy(chi, diag_lin, h, lam, weight=None):
    w = np.ones(chi.size) if weight is None else weight
    d = np.diff(np.r_[0.0, chi, 0.0]) / h
    return float(h * (0.5 * np.sum(d**2) + np.sum(0.5 * diag_lin * chi**2 + 0.25 * lam * w * chi**4)))


def solve_static(diag_lin, h, lam, bulk_guess, weight=None):
    """Return (chi, E, eps0, psi0): minimiser, its energy, lowest eigenvalue/eigenvector of the linear operator."""
    n = diag_lin.size
    ev, vec = eigh_tridiagonal(2.0 / h**2 + diag_lin, -np.ones(n - 1) / h**2, select="i", select_range=(0, 0))
    eps0, psi = float(ev[0]), vec[:, 0] * np.sign(vec[np.argmax(np.abs(vec[:, 0])), 0])
    if eps0 >= 0:
        return np.zeros(n), 0.0, eps0, psi           # closed gate is the (unique) minimiser
    w = np.ones(n) if weight is None else weight
    amp = np.sqrt(-eps0 * np.sum(psi**2) / (lam * np.sum(w * psi**4)))
    best = (np.zeros(n), 0.0)
    for guess in (bulk_guess, amp * psi):
        chi = newton(guess.copy(), diag_lin, h, lam, weight)
        e = energy(chi, diag_lin, h, lam, weight)
        if e < best[1]:
            best = (chi, e)
    return best[0], best[1], eps0, psi


def slab(L, r, lam, h=0.01, pad=16.0):
    X = L / 2 + pad
    n = int(round(2 * X / h))
    x = -X + (np.arange(n) + 0.5) * h
    inside = np.abs(x) < L / 2
    diag = 1.0 - r * inside
    chi, e, eps0, psi = solve_static(diag, h, lam, np.sqrt((r - 1) / lam) * inside)
    wnl = (eps0**2 * (h * np.sum(psi**2)) ** 2 / (4 * lam * h * np.sum(psi**4))) if eps0 < 0 else 0.0
    return {"x": x, "chi": chi, "W": -e, "eps0": eps0, "W_weakly_nonlinear": float(wnl)}


def ball(R, r, lam, h=0.01, pad=16.0):
    n = int(round((R + pad) / h)) - 1
    rho = (np.arange(n) + 1.0) * h
    inside = np.where(rho < R - 1e-12, 1.0, np.where(np.abs(rho - R) <= 1e-12, 0.5, 0.0))
    diag = 1.0 - r * inside
    # unknown is u = rho*chi; quartic term carries weight 1/rho^2; energies get the factor 4 pi
    u, e, eps0, psi = solve_static(diag, h, lam, np.sqrt((r - 1) / lam) * inside * rho, weight=1.0 / rho**2)
    return {"rho": rho, "chi": u / rho, "W": -4 * np.pi * e, "eps0": eps0}


def main() -> int:
    plt = setup_matplotlib()
    r, lam = 5.0, 1.0
    u_bulk = (r - 1) ** 2 / (4 * lam)
    Lc, Rc = float(Lc_slab(r)), float(Rc_ball(r))
    out: dict = {"r": r, "lambda": lam, "u_bulk": u_bulk, "Lc": Lc, "Rc": Rc}
    print(f"r = {r}, lambda = {lam}:  bulk energy density u = {u_bulk},  L_c = {Lc:.5f},  R_c = {Rc:.5f}")

    # ------------------------------------------------------------------ slab: W(L)
    Ls = np.unique(np.round(np.r_[np.linspace(0.2, 0.44, 4), Lc + np.geomspace(0.02, 12.0, 26)], 2))
    rows = []
    with Timer("slab W(L)"):
        for L in Ls:
            s = slab(L, r, lam)
            rows.append({"L": float(L), "W": s["W"], "bulk_bound": u_bulk * L, "eps0": s["eps0"],
                         "W_weakly_nonlinear": s["W_weakly_nonlinear"]})
    W = np.array([q["W"] for q in rows])
    Lv = np.array([q["L"] for q in rows])
    bound_ok = bool(np.all(W <= u_bulk * Lv + 1e-10))
    closed_ok = bool(np.all(W[Lv < Lc - 1e-9] == 0.0))
    mono_ok = bool(np.all(np.diff(W) >= -1e-10))
    force = np.gradient(W, Lv)
    conv_ok = bool(np.all(np.diff(force[Lv > Lc]) >= -5e-3))        # convexity: force non-decreasing
    asym = force[-1] / u_bulk
    print(f"   W = 0 for all L < L_c: {closed_ok};  W <= u L everywhere: {bound_ok};  W non-decreasing: {mono_ok};"
          f"  convex (force non-decreasing): {conv_ok}")
    print(f"   force per unit area at L = {Lv[-1]:.1f}:  dW/dL = {force[-1]:.5f}  = {asym:.5f} x bulk value u")
    # weakly nonlinear check close to threshold
    near = [q for q in rows if 0 < q["L"] - Lc < 0.08]
    for q in near:
        print(f"   near threshold L-L_c={q['L']-Lc:.3f}: W={q['W']:.4e}  weakly-nonlinear prediction={q['W_weakly_nonlinear']:.4e}"
              f"  ratio={q['W']/q['W_weakly_nonlinear']:.3f}")
    out["slab"] = {"rows": rows, "W_zero_below_threshold": closed_ok, "bulk_bound_holds": bound_ok,
                   "monotone": mono_ok, "convex": conv_ok, "asymptotic_force_over_u": float(asym)}

    # grid convergence of W at one L
    conv = []
    for h in (0.04, 0.02, 0.01, 0.005):
        conv.append({"h": h, "W": slab(4.0, r, lam, h=h)["W"]})
    ref = conv[-1]["W"]
    errs = [abs(c["W"] - ref) for c in conv[:-1]]
    print("   grid convergence of W(L=4):", ", ".join(f"h={c['h']}: {c['W']:.8f}" for c in conv),
          "| successive error ratio:", np.round([errs[i] / errs[i + 1] for i in range(len(errs) - 1)], 2))
    out["slab"]["convergence"] = conv

    # ------------------------------------------------------------------ ball: W(R)
    Rv = np.unique(np.round(np.r_[np.linspace(0.3, Rc - 0.05, 4), Rc + np.geomspace(0.03, 9.0, 18)], 2))
    brow = []
    with Timer("ball W(R)"):
        for R in Rv:
            b = ball(R, r, lam)
            brow.append({"R": float(R), "W": b["W"], "bulk_bound": u_bulk * 4 * np.pi * R**3 / 3, "eps0": b["eps0"]})
    WB = np.array([q["W"] for q in brow])
    bb_ok = bool(np.all(WB <= np.array([q["bulk_bound"] for q in brow]) + 1e-9))
    bclosed = bool(np.all(WB[Rv < Rc - 1e-9] == 0.0))
    print(f"   ball: W = 0 for R < R_c: {bclosed};  W <= u * volume: {bb_ok};  W/(u V) at R={Rv[-1]:.1f}: "
          f"{WB[-1]/brow[-1]['bulk_bound']:.4f}")
    out["ball"] = {"rows": brow, "W_zero_below_threshold": bclosed, "bulk_bound_holds": bb_ok}

    # ------------------------------------------------------------------ figure
    fig, axs = plt.subplots(1, 3, figsize=(15.5, 4.3))
    ax = axs[0]
    for L, col, ls in ((0.9, AQUA, ":"), (2.0, ORANGE, (0, (6, 3))), (8.0, BLUE, "-")):
        s = slab(L, r, lam)
        ax.plot(s["x"], s["chi"], color=col, ls=ls, label=f"overlap width L = {L}")
    ax.axhline(np.sqrt((r - 1) / lam), color=INK2, lw=0.8)
    ax.text(-9.6, np.sqrt((r - 1) / lam) + 0.04, "bulk value", color=INK2, fontsize=8)
    ax.set_xlim(-10, 10); ax.set_xlabel("x  [1/$\\mu$]"); ax.set_ylabel("gate field $\\chi$")
    ax.set_ylim(-0.1, 3.0)
    ax.set_title("Open-gate profiles (static)"); ax.legend(loc="upper right")

    ax = axs[1]
    ax.plot(Lv, W, color=BLUE, label="binding energy W (numerical)")
    ax.plot(Lv, u_bulk * Lv, color=ORANGE, ls=(0, (6, 3)), label="rigorous bulk bound  $u\\,L$")
    ax.axvline(Lc, color=INK2, lw=0.8)
    ax.text(Lc + 0.15, 0.82 * u_bulk * Lv[-1], "threshold $L_c$", color=INK2, fontsize=8)
    ax.set_xlabel("overlap width L  [1/$\\mu$]"); ax.set_ylabel("energy per unit area")
    ax.set_title("Binding energy: zero, then bounded by bulk"); ax.legend(loc="upper left", bbox_to_anchor=(0.12, 0.8))

    ax = axs[2]
    ax.plot(Lv, force / u_bulk, color=BLUE)
    ax.axhline(1.0, color=ORANGE, lw=1.4, ls=(0, (6, 3)))
    ax.text(Lv[-1], 1.03, "bulk traction u", color=INK2, fontsize=8, ha="right")
    ax.axvline(Lc, color=INK2, lw=0.8)
    ax.set_ylim(-0.05, 1.15)
    ax.set_xlabel("overlap width L  [1/$\\mu$]"); ax.set_ylabel("attractive force per area,  (dW/dL) / u")
    ax.set_title("Contact force: none below $L_c$, a pull above")
    fig.savefig("results/exp3_static_gate_energy.png")
    plt.close(fig)

    save_json("exp3_static_gate_energy.json", out)
    wn_ok = all(abs(q["W"] / q["W_weakly_nonlinear"] - 1) < 0.25 for q in near) if near else True
    ok = closed_ok and bound_ok and mono_ok and bb_ok and bclosed and abs(asym - 1) < 0.01 and wn_ok
    print("RESULT:", "consistent with Theorem 3" if ok else "CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
