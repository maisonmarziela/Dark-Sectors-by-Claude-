"""Experiment 1 - conservation laws and causality for a gated cross-sector coupling (1+1D).

Model (units hbar = c = 1; all quantities dimensionless):

    L = sum_{X=A,B} [ 1/2 (d phi_X)^2 - 1/2 m_X^2 phi_X^2 ]  -  1/2 f(t,x) phi_A^2 phi_B^2

i.e. O_A = phi_A^2, O_B = phi_B^2, gate function F = f/2.

Part (a)  PRESCRIBED gate f(t,x) (a non-dynamical pulse).  The manuscript's
          Proposition 2 says A+B energy-momentum is then NOT conserved and that
              Delta P_{A+B}        = - int dt dx (d_x f) 1/2 phi_A^2 phi_B^2
              Delta (E_A+E_B+E_int) = + int dt dx (d_t f) 1/2 phi_A^2 phi_B^2 .
          We measure both sides independently and check they agree, with a
          resolution study.
Part (b)  DYNAMICAL gate  f = g chi^2  with chi a third field.  Total energy
          and momentum are conserved; whatever A+B lose is carried by chi.
Part (c)  CAUSALITY.  With a gate of strictly compact spacetime support, the
          difference between the coupled and the uncoupled evolution must
          vanish outside the future light cone of the gate's support.

All of this tests the *internal consistency of the equations*.  None of it is
evidence about nature.
"""
from __future__ import annotations

import numpy as np

from crh_common import (AQUA, BLUE, INK2, MUTED, ORANGE, Timer, field_energy, field_momentum, grad_c, lap, save_json,
                        setup_matplotlib)

MA2, MB2 = 1.0, 1.44      # m_A^2, m_B^2
LBOX = 240.0


def packet(x, x0, k, w, amp, m2, direction):
    """Approximately one-way-moving wave packet (phi, pi) of a massive field."""
    om = np.sqrt(k * k + m2)
    env = amp * np.exp(-((x - x0) ** 2) / (2 * w * w))
    ph = k * (x - x0)
    phi = env * np.cos(ph)
    pi = direction * om * env * np.sin(ph)          # d_t [env cos(k x - s om t)] at t=0, s=direction
    return phi, pi


# ----------------------------------------------------------------------------------------------
def run_prescribed(n: int, cfl: float = 0.4, f0: float = 0.8, t_end: float = 110.0):
    dx = LBOX / n
    x = (np.arange(n) + 0.5) * dx - LBOX / 2
    dt = cfl * dx
    nsteps = int(round(t_end / dt))
    dt = t_end / nsteps

    a, pa = packet(x, -35.0, 1.2, 6.0, 1.0, MA2, +1)
    b, pb = packet(x, +35.0, 1.0, 6.0, 1.0, MB2, -1)

    # gate pulse: displaced from the collision point and tilted in spacetime so that both
    # d_x f and d_t f have non-trivial overlap with phi_A^2 phi_B^2
    xg, tg, sx, st, vg = 4.0, 43.0, 7.0, 9.0, 0.25

    def f(tt):
        return f0 * np.exp(-((x - xg - vg * (tt - tg)) ** 2) / (2 * sx * sx) - ((tt - tg) ** 2) / (2 * st * st))

    def dfdx(tt):
        return -f(tt) * (x - xg - vg * (tt - tg)) / (sx * sx)

    def dfdt(tt):
        return f(tt) * (vg * (x - xg - vg * (tt - tg)) / (sx * sx) - (tt - tg) / (st * st))

    def forces(a, b, tt):
        ff = f(tt)
        return lap(a, dx) - MA2 * a - ff * a * b * b, lap(b, dx) - MB2 * b - ff * a * a * b

    def observables(a, pa, b, pb, tt):
        e = field_energy(a, pa, MA2, dx) + field_energy(b, pb, MB2, dx) + dx * np.sum(0.5 * f(tt) * a * a * b * b)
        p = field_momentum(a, pa, dx) + field_momentum(b, pb, dx)
        return e, p

    e0, p0 = observables(a, pa, b, pb, 0.0)
    IP = IE = 0.0                                   # trapezoid accumulators for the source integrals
    srcP = -dx * np.sum(dfdx(0.0) * 0.5 * a * a * b * b)
    srcE = +dx * np.sum(dfdt(0.0) * 0.5 * a * a * b * b)
    fa, fb = forces(a, b, 0.0)
    ts, es, ps = [0.0], [e0], [p0]
    for i in range(nsteps):
        tt = i * dt
        pa += 0.5 * dt * fa
        pb += 0.5 * dt * fb
        a += dt * pa
        b += dt * pb
        fa, fb = forces(a, b, tt + dt)
        pa += 0.5 * dt * fa
        pb += 0.5 * dt * fb
        nP = -dx * np.sum(dfdx(tt + dt) * 0.5 * a * a * b * b)
        nE = +dx * np.sum(dfdt(tt + dt) * 0.5 * a * a * b * b)
        IP += 0.5 * dt * (srcP + nP)
        IE += 0.5 * dt * (srcE + nE)
        srcP, srcE = nP, nE
        if (i + 1) % max(1, nsteps // 400) == 0 or i == nsteps - 1:
            e, p = observables(a, pa, b, pb, tt + dt)
            ts.append(tt + dt), es.append(e), ps.append(p)
    e1, p1 = observables(a, pa, b, pb, t_end)
    return {"n": n, "dx": dx, "dt": dt, "E0": e0, "P0": p0, "dE": e1 - e0, "dP": p1 - p0,
            "IE": IE, "IP": IP, "errE": abs((e1 - e0) - IE), "errP": abs((p1 - p0) - IP),
            "t": ts, "E": es, "P": ps}


# ----------------------------------------------------------------------------------------------
def run_dynamical(n: int, cfl: float = 0.4, g: float = 0.8, t_end: float = 110.0, mc2: float = 0.64):
    dx = LBOX / n
    x = (np.arange(n) + 0.5) * dx - LBOX / 2
    dt = cfl * dx
    nsteps = int(round(t_end / dt))
    dt = t_end / nsteps
    a, pa = packet(x, -35.0, 1.2, 6.0, 1.0, MA2, +1)
    b, pb = packet(x, +35.0, 1.0, 6.0, 1.0, MB2, -1)
    c = 1.2 * np.exp(-((x - 4.0) ** 2) / (2 * 7.0**2))     # pre-existing lump of gate field
    pc = np.zeros(n)

    def forces(a, b, c):
        return (lap(a, dx) - MA2 * a - g * c * c * a * b * b,
                lap(b, dx) - MB2 * b - g * c * c * a * a * b,
                lap(c, dx) - mc2 * c - g * c * a * a * b * b)

    def obs(a, pa, b, pb, c, pc):
        eint = dx * np.sum(0.5 * g * c * c * a * a * b * b)
        E = field_energy(a, pa, MA2, dx) + field_energy(b, pb, MB2, dx) + field_energy(c, pc, mc2, dx) + eint
        PA, PB, PC = field_momentum(a, pa, dx), field_momentum(b, pb, dx), field_momentum(c, pc, dx)
        return E, PA, PB, PC

    fa, fb, fc = forces(a, b, c)
    rec = [(0.0, *obs(a, pa, b, pb, c, pc))]
    for i in range(nsteps):
        pa += 0.5 * dt * fa; pb += 0.5 * dt * fb; pc += 0.5 * dt * fc
        a += dt * pa; b += dt * pb; c += dt * pc
        fa, fb, fc = forces(a, b, c)
        pa += 0.5 * dt * fa; pb += 0.5 * dt * fb; pc += 0.5 * dt * fc
        if (i + 1) % max(1, nsteps // 400) == 0 or i == nsteps - 1:
            rec.append(((i + 1) * dt, *obs(a, pa, b, pb, c, pc)))
    rec = np.array(rec)
    E, PA, PB, PC = rec[:, 1], rec[:, 2], rec[:, 3], rec[:, 4]
    Ptot = PA + PB + PC
    return {"n": n, "dx": dx, "t": rec[:, 0], "E": E, "PA": PA, "PB": PB, "PC": PC,
            "max_dE_rel": float(np.max(np.abs(E - E[0])) / abs(E[0])),
            "max_dPtot": float(np.max(np.abs(Ptot - Ptot[0]))),
            "dP_AB": float((PA + PB)[-1] - (PA + PB)[0]), "dP_gate": float(PC[-1] - PC[0])}


# ----------------------------------------------------------------------------------------------
def run_causality(n: int, cfl: float = 0.5, f0: float = 1.5, t_end: float = 60.0, store: bool = False):
    dx = LBOX / n
    x = (np.arange(n) + 0.5) * dx - LBOX / 2
    dt = cfl * dx
    nsteps = int(round(t_end / dt))
    dt = t_end / nsteps
    # smooth, everywhere-nonzero backgrounds in both sectors (periodic standing waves)
    kA, kB = 2 * np.pi * 9 / LBOX, 2 * np.pi * 7 / LBOX
    a0, b0 = 0.9 * np.cos(kA * x) + 0.3, 0.8 * np.sin(kB * x) + 0.4
    xg, tg, ax, at = 0.0, 12.0, 6.0, 5.0             # gate support: |x-xg|<ax, |t-tg|<at

    def f(tt):
        if abs(tt - tg) >= at:
            return np.zeros(n)
        sx = np.where(np.abs(x - xg) < ax, np.cos(np.pi * (x - xg) / (2 * ax)) ** 4, 0.0)
        return f0 * sx * np.cos(np.pi * (tt - tg) / (2 * at)) ** 4

    def evolve(coupled: bool):
        a, b = a0.copy(), b0.copy()
        pa, pb = np.zeros(n), np.zeros(n)
        frames = []

        def forces(a, b, tt):
            ff = f(tt) if coupled else 0.0
            return lap(a, dx) - MA2 * a - ff * a * b * b, lap(b, dx) - MB2 * b - ff * a * a * b

        fa, fb = forces(a, b, 0.0)
        every = max(1, nsteps // 240)
        for i in range(nsteps):
            pa += 0.5 * dt * fa; pb += 0.5 * dt * fb
            a += dt * pa; b += dt * pb
            fa, fb = forces(a, b, (i + 1) * dt)
            pa += 0.5 * dt * fa; pb += 0.5 * dt * fb
            if (i + 1) % every == 0:
                frames.append(((i + 1) * dt, a.copy()))
        return frames

    fc, fu = evolve(True), evolve(False)
    t_on = tg - at
    out_max, in_max, margin = 0.0, 0.0, 1.0
    img, times = [], []
    for (tt, ac), (_, au) in zip(fc, fu):
        d = np.abs(ac - au)
        reach = ax + max(0.0, tt - t_on)             # edge of the causal future of the gate support
        outside = np.abs(x - xg) > reach + margin
        if tt <= t_on:
            outside = np.ones(n, bool)
        # stop once the future cone wraps around the periodic box
        if reach + margin < LBOX / 2:
            out_max = max(out_max, float(d[outside].max()) if outside.any() else 0.0)
        in_max = max(in_max, float(d.max()))
        if store:
            img.append(d), times.append(tt)
    res = {"n": n, "dx": dx, "dt": dt, "max_diff_inside": in_max, "max_diff_outside_cone": out_max,
           "ratio": out_max / in_max if in_max else 0.0}
    if store:
        res["img"] = np.array(img); res["times"] = np.array(times); res["x"] = x
        res["gate"] = (xg, tg, ax, at)
    return res


# ----------------------------------------------------------------------------------------------
def main() -> int:
    plt = setup_matplotlib()
    summary: dict = {}

    print("(a) prescribed gate: measured non-conservation vs Proposition 2")
    rows = []
    with Timer("prescribed-gate resolution study"):
        for n in (1200, 2400, 4800, 9600):
            r = run_prescribed(n)
            rows.append(r)
            print(f"   n={n:5d} dx={r['dx']:.4f}  dP={r['dP']:+.6e}  formula={r['IP']:+.6e}  |err|={r['errP']:.2e}"
                  f"   dE={r['dE']:+.6e}  formula={r['IE']:+.6e}  |err|={r['errE']:.2e}")
    ordP = [np.log2(rows[i]["errP"] / rows[i + 1]["errP"]) for i in range(len(rows) - 1)]
    ordE = [np.log2(rows[i]["errE"] / rows[i + 1]["errE"]) for i in range(len(rows) - 1)]
    print(f"   observed convergence order: momentum {np.round(ordP, 2)}, energy {np.round(ordE, 2)} (expected 2)")
    best = rows[-1]
    summary["prescribed_gate"] = {
        "rows": [{k: r[k] for k in ("n", "dx", "dP", "IP", "errP", "dE", "IE", "errE")} for r in rows],
        "order_momentum": ordP, "order_energy": ordE,
        "relative_violation_of_momentum": abs(best["dP"]) / abs(best["P0"]),
        "relative_violation_of_energy": abs(best["dE"]) / abs(best["E0"]),
        "relative_mismatch_formula_P": best["errP"] / abs(best["dP"]),
        "relative_mismatch_formula_E": best["errE"] / abs(best["dE"]),
    }

    print("(b) dynamical gate: total conservation")
    with Timer("dynamical gate"):
        dyn = [run_dynamical(n) for n in (2400, 4800, 9600)]
    for d in dyn:
        print(f"   n={d['n']}: max|dE|/E = {d['max_dE_rel']:.2e}   max|dP_tot| = {d['max_dPtot']:.2e}"
              f"   dP_(A+B) = {d['dP_AB']:+.5e}   dP_gate = {d['dP_gate']:+.5e}")
    summary["dynamical_gate"] = [{k: d[k] for k in ("n", "dx", "max_dE_rel", "max_dPtot", "dP_AB", "dP_gate")} for d in dyn]

    print("(c) causality: coupled-minus-uncoupled difference outside the gate's future light cone")
    with Timer("causality"):
        caus = [run_causality(n, store=(n == 4800)) for n in (1200, 2400, 4800)]
    for c in caus:
        print(f"   n={c['n']}: max diff inside = {c['max_diff_inside']:.3e}   outside cone = "
              f"{c['max_diff_outside_cone']:.3e}   ratio = {c['ratio']:.2e}")
    summary["causality"] = [{k: c[k] for k in ("n", "dx", "max_diff_inside", "max_diff_outside_cone", "ratio")} for c in caus]

    # ------------------------------------------------------------------ figures
    fig, axs = plt.subplots(1, 3, figsize=(15.5, 4.4))
    ax = axs[0]
    t = np.array(best["t"])
    ax.plot(t, np.array(best["P"]) - best["P0"], color=BLUE, label="measured  $P_A+P_B$ change")
    ax.axhline(best["IP"], color=ORANGE, lw=1.6, ls=(0, (6, 3)), label="Prop. 2 formula (final value)")
    ax.set_title("Prescribed gate: momentum is NOT conserved")
    ax.set_xlabel("time  [1/m$_A$]"); ax.set_ylabel("$\\Delta(P_A+P_B)$")
    ax.legend(loc="best")

    ax = axs[1]
    d = dyn[-1]
    ax.plot(d["t"], d["PA"] + d["PB"] - (d["PA"] + d["PB"])[0], color=BLUE, label="sectors A+B")
    ax.plot(d["t"], d["PC"] - d["PC"][0], color=ORANGE, ls=(0, (6, 3)), label="gate field $\\chi$")
    ax.plot(d["t"], (d["PA"] + d["PB"] + d["PC"]) - (d["PA"] + d["PB"] + d["PC"])[0], color=AQUA, ls=":", lw=2.4,
            label="total")
    ax.set_title("Dynamical gate: the gate carries the balance")
    ax.set_xlabel("time  [1/m$_A$]"); ax.set_ylabel("momentum change")
    ax.legend(loc="best")

    ax = axs[2]
    c = caus[-1]
    xg, tg, axg, atg = c["gate"]
    img = np.log10(np.maximum(c["img"], 1e-18))
    pm = ax.pcolormesh(c["x"], c["times"], img, cmap="Blues", vmin=-16, vmax=np.log10(c["max_diff_inside"]),
                       shading="auto", rasterized=True)
    tt = np.linspace(tg - atg, c["times"][-1], 50)
    for sgn in (-1, 1):
        ax.plot(xg + sgn * (axg + (tt - (tg - atg))), tt, color=ORANGE, lw=1.6)
    ax.add_patch(plt.Rectangle((xg - axg, tg - atg), 2 * axg, 2 * atg, fill=False, ec=INK2, lw=1.2))
    ax.annotate("gate region", xy=(xg - axg, tg), xytext=(-62, tg), fontsize=9, color=INK2, va="center",
                arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    ax.text(xg + axg + 26, tg + 14, "light cone", color=INK2, fontsize=9, rotation=38)
    ax.set_xlim(-90, 90); ax.grid(False)
    ax.set_title("Causality: disturbance stays inside the light cone")
    ax.set_xlabel("position x"); ax.set_ylabel("time")
    cb = fig.colorbar(pm, ax=ax, pad=0.02)
    cb.set_label("log$_{10}$ |$\\phi_A^{coupled}-\\phi_A^{uncoupled}$|", color=INK2)
    cb.outline.set_edgecolor(MUTED)
    fig.savefig("results/exp1_conservation_causality.png")
    plt.close(fig)

    save_json("exp1_conservation_causality.json", summary)
    ok = (summary["prescribed_gate"]["relative_mismatch_formula_P"] < 1e-3
          and summary["prescribed_gate"]["relative_mismatch_formula_E"] < 1e-3
          and dyn[-1]["max_dE_rel"] < 1e-3 and caus[-1]["ratio"] < 1e-6)
    print("RESULT:", "consistent with Propositions 1-2 and causality" if ok else "CHECK FAILED - see numbers above")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
