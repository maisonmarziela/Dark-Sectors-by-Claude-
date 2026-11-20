"""Experiment 5 - how "silent" is a contact event?  Gate radiation versus switching time.

Requirement 2 of the thought experiment says the event should not launch a propagating
disturbance.  In the overlap-triggered gate model the gate field has a mass gap mu, so a slowly
varying overlap might be expected to emit exponentially little.  It does not: the opening and the
closing of the gate each pass through a critical point where the gate's lowest mode is gapless,
so adiabaticity necessarily fails there (the Kibble-Zurek situation).  A scaling argument
(manuscript Sec. 6.5) for a linear passage through threshold predicts

        E_radiated / W_peak  ~  C (mu tau)^(-4/3)      (up to logarithms of the seed amplitude)
        opening delay        ~  tau^(1/3)

This script measures both, for a fixed slab of overlap whose ratio r(t) is ramped
0 -> r_max -> 0 with a smooth profile of duration tau each way.

Units mu = 1.  E_radiated is the energy left in free gate quanta after the overlap is gone
(absorbed by the boundary sponge + still in the box).
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

from crh_common import BLUE, INK2, ORANGE, Timer, save_json, setup_matplotlib, smooth_noise
from exp2_gate_threshold import Lc_slab
from exp3_static_gate_energy import slab

LAM, R_MAX, L_SLAB = 1.0, 5.0, 10.0
XMAX, SPONGE, T_HOLD = 120.0, 40.0, 100.0


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * u * (10.0 - 15.0 * u + 6.0 * u * u)


def run(tau: float, seed_amp: float = 1e-6, rng_seed: int = 0, dx: float = 0.1, cfl: float = 0.4):
    n = int(round(2 * XMAX / dx))
    x = -XMAX + (np.arange(n) + 0.5) * dx
    dt = cfl * dx
    t_end = 2 * tau + T_HOLD + 20.0
    nsteps = int(round(t_end / dt))
    dt = t_end / nsteps
    inside = (np.abs(x) < L_SLAB / 2).astype(float)
    gam = np.where(np.abs(x) > XMAX - SPONGE, 0.5 * ((np.abs(x) - (XMAX - SPONGE)) / SPONGE) ** 2, 0.0)
    damp, sp = np.exp(-gam * dt / 2), gam > 0

    def r_of_t(t):
        return R_MAX * (smoothstep(t / tau) - smoothstep((t - tau - T_HOLD) / tau))

    rng = np.random.default_rng(rng_seed)
    chi, pi = smooth_noise(rng, n, dx, seed_amp, kmax=3.0), np.zeros(n)

    def force(chi, t):
        return (np.roll(chi, -1) - 2 * chi + np.roll(chi, 1)) / dx**2 - (1.0 - r_of_t(t) * inside) * chi - LAM * chi**3

    def field_E(chi, pi):
        d = (np.roll(chi, -1) - chi) / dx
        return dx * np.sum(0.5 * pi**2 + 0.5 * d**2 + 0.5 * chi**2 + 0.25 * LAM * chi**4)

    E_sponge, t_on = 0.0, np.nan
    f = force(chi, 0.0)
    for i in range(nsteps):
        t = i * dt
        b = pi[sp].copy(); pi *= damp; E_sponge += 0.5 * dx * np.sum(b**2 - pi[sp] ** 2)
        pi += 0.5 * dt * f
        chi += dt * pi
        f = force(chi, t + dt)
        pi += 0.5 * dt * f
        b = pi[sp].copy(); pi *= damp; E_sponge += 0.5 * dx * np.sum(b**2 - pi[sp] ** 2)
        if np.isnan(t_on) and (i % 5 == 0) and np.max(np.abs(chi)) > 0.2:
            t_on = t + dt
    E_rad = field_E(chi, pi) + E_sponge
    return {"tau": tau, "seed_amp": seed_amp, "rng_seed": rng_seed, "E_rad": float(E_rad), "t_on": float(t_on)}


def main() -> int:
    plt = setup_matplotlib()
    W_peak = slab(L_SLAB, R_MAX, LAM)["W"]
    r_c = brentq(lambda r: Lc_slab(r) - L_SLAB, 1.0 + 1e-12, 1e3)        # threshold ratio for this slab
    print(f"slab L = {L_SLAB}, r_max = {R_MAX}:  static binding energy W_peak = {W_peak:.4f};"
          f"  threshold ratio r_c = {r_c:.5f}")
    out: dict = {"W_peak": W_peak, "r_c": r_c, "L": L_SLAB, "r_max": R_MAX}

    taus = [12.5, 25.0, 50.0, 100.0, 200.0, 400.0, 800.0, 1600.0]
    seeds = [0, 1, 2]
    rows = []
    with Timer("tau sweep (3 seeds each)"):
        for tau in taus:
            rs = [run(tau, rng_seed=s) for s in seeds]
            frac = np.array([q["E_rad"] for q in rs]) / W_peak
            # time at which r(t) crosses the threshold on the way up, and the delay of the opening
            t_c = brentq(lambda t: R_MAX * smoothstep(t / tau) - r_c, 0.0, tau)
            delay = np.array([q["t_on"] for q in rs]) - t_c
            rows.append({"tau": tau, "frac_mean": float(frac.mean()), "frac_min": float(frac.min()),
                         "frac_max": float(frac.max()), "t_c": float(t_c), "delay_mean": float(np.nanmean(delay)),
                         # rate of passage through threshold d r / d t at t_c
                         "ramp_rate": float(R_MAX * 30 * (t_c / tau) ** 2 * (1 - t_c / tau) ** 2 / tau)})
            print(f"   tau={tau:7.1f}: E_rad/W_peak = {frac.mean():.3e}  (range {frac.min():.2e} - {frac.max():.2e})"
                  f"   opening delay = {np.nanmean(delay):6.2f}")
    out["tau_sweep"] = rows

    tau_a = np.array([q["tau"] for q in rows])
    fr = np.array([q["frac_mean"] for q in rows])
    dl = np.array([q["delay_mean"] for q in rows])
    big = tau_a >= 100.0
    (slope_E, icpt_E), covE = np.polyfit(np.log(tau_a[big]), np.log(fr[big]), 1, cov=True)
    (slope_D, icpt_D), covD = np.polyfit(np.log(tau_a[big]), np.log(dl[big]), 1, cov=True)
    sE, sD = float(np.sqrt(covE[0, 0])), float(np.sqrt(covD[0, 0]))
    local = np.diff(np.log(fr)) / np.diff(np.log(tau_a))          # local log-slopes between neighbouring tau
    print(f"   fitted scaling for tau >= 100:  E_rad/W_peak ~ tau^({slope_E:.2f} +- {sE:.2f})"
          f"   (scaling argument: -4/3 = -1.33)")
    print(f"                                   opening delay ~ tau^({slope_D:.2f} +- {sD:.2f})"
          f"   (scaling argument: +1/3 = +0.33)")
    print(f"   local log-slopes of the radiated fraction between neighbouring tau: {np.round(local, 2)}")
    out["fit"] = {"energy_exponent": float(slope_E), "energy_exponent_stderr": sE,
                  "energy_prefactor": float(np.exp(icpt_E)), "delay_exponent": float(slope_D),
                  "delay_exponent_stderr": sD, "local_energy_slopes": local,
                  "predicted_energy_exponent": -4 / 3, "predicted_delay_exponent": 1 / 3}

    print("   dependence on the (unphysical) classical seed amplitude at tau = 200:")
    srows = []
    with Timer("seed sweep"):
        for amp in (1e-3, 1e-5, 1e-7, 1e-9, 1e-11):
            q = run(200.0, seed_amp=amp, rng_seed=0)
            srows.append({"seed_amp": amp, "frac": q["E_rad"] / W_peak})
            print(f"      seed {amp:.0e}:  E_rad/W_peak = {q['E_rad'] / W_peak:.3e}")
    out["seed_sweep"] = srows
    sa = np.array([q["seed_amp"] for q in srows]); sf = np.array([q["frac"] for q in srows])
    seed_slope = float(np.polyfit(np.log(1 / sa), np.log(sf), 1)[0])
    print(f"      effective power of ln-dependence: d ln(frac) / d ln(1/seed) = {seed_slope:.3f} (weak, logarithmic)")
    out["seed_sensitivity"] = seed_slope

    print("   grid check at tau = 100 (same seed):")
    g = []
    for dx in (0.2, 0.1, 0.05):
        q = run(100.0, dx=dx)
        g.append({"dx": dx, "frac": q["E_rad"] / W_peak})
        print(f"      dx = {dx}: E_rad/W_peak = {q['E_rad'] / W_peak:.4e}")
    out["grid_check"] = g

    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.4))
    ax = axs[0]
    lo = np.array([q["frac_min"] for q in rows]); hi = np.array([q["frac_max"] for q in rows])
    ax.errorbar(tau_a, fr, yerr=[fr - lo, hi - fr], fmt="o", color=BLUE, mec="white", mew=1.5, capsize=3,
                label="simulation (mean and range of 3 seeds)")
    tt = np.geomspace(60, 2200, 50)
    ax.plot(tt, np.exp(icpt_E) * tt**slope_E, color=BLUE, lw=1.4, label=f"fit  $\\tau^{{{slope_E:.2f}}}$")
    ax.plot(tt, fr[big][0] * (tt / tau_a[big][0]) ** (-4 / 3), color=ORANGE, lw=1.6, ls=(0, (6, 3)),
            label="scaling argument  $\\tau^{-4/3}$")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("switching time $\\tau$  [1/$\\mu$]"); ax.set_ylabel("radiated energy / peak gate energy")
    ax.set_title("Gate radiation falls as a power law, not exponentially"); ax.legend(loc="lower left")

    ax = axs[1]
    ax.loglog(tau_a, dl, "o", color=BLUE, mec="white", mew=1.5, label="simulation")
    ax.plot(tt, np.exp(icpt_D) * tt**slope_D, color=BLUE, lw=1.4, label=f"fit  $\\tau^{{{slope_D:.2f}}}$")
    ax.plot(tt, dl[big][0] * (tt / tau_a[big][0]) ** (1 / 3), color=ORANGE, lw=1.6, ls=(0, (6, 3)),
            label="scaling argument  $\\tau^{1/3}$")
    ax.set_xlabel("switching time $\\tau$  [1/$\\mu$]"); ax.set_ylabel("delay of gate opening after threshold  [1/$\\mu$]")
    ax.set_title("Opening lags the threshold crossing"); ax.legend(loc="upper left")
    ax.text(0.98, 0.04, "seed amplitude $10^{-6}$", transform=ax.transAxes, ha="right", fontsize=8, color=INK2)
    fig.savefig("results/exp5_adiabatic_radiation.png")
    plt.close(fig)

    save_json("exp5_adiabatic_radiation.json", out)
    mono = bool(np.all(np.diff(fr[big]) < 0))
    print("RESULT:", f"radiated fraction decreases monotonically for tau >= 100: {mono};"
          f" exponent {slope_E:.2f} vs predicted -1.33; delay exponent {slope_D:.2f} vs predicted 0.33")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
