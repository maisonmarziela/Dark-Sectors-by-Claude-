"""Experiment 4 - a complete "contact event" with an overlap-triggered gate (1+1D, dynamical).

Cast
  * body A  : a rigid slab of sector-A matter (the observer's skin), mass M_A, held by a damped
              spring (tissue elasticity).  Fully dynamical.
  * body B  : a rigid slab of sector-B matter (the visitor's hand).  Its trajectory X_B(t) is
              prescribed: approach - hold - retract.  The force the gate exerts on it is recorded;
              it is what B's "muscles" must balance, i.e. what the B observer feels.
  * gate chi: a real scalar field with the even ("threshold") coupling

        chi_tt = chi_xx - mu^2 [1 - r0 n_A(x - X_A) n_B(x - X_B)] chi - lambda chi^3 .

Units mu = 1.  n_A, n_B are smooth top-hat profiles in [0, 1]; r0 is the overlap ratio at full
overlap.  The interaction energy is  E_int = -(1/2) mu^2 r0 int chi^2 n_A n_B dx.

What is checked
  1. BASELINE (r0 = 0): A does not move at all.
  2. SUB-THRESHOLD densities (r0 < 1) and SUB-CRITICAL overlap size: the gate never opens and A
     does not move - isolation is exact up to the decaying seed.
  3. CONTACT (r0 = 5): the gate opens only once the overlap exceeds the critical size; A is pulled
     toward B with the bulk traction u = mu^4 (r0-1)^2 / 4 lambda; the gate force on B is equal and
     opposite up to the momentum carried by chi (Newton's third law including the gate).
  4. After retraction the gate closes again: no residual coupling, chi returns to (near) zero.
  5. Energy and momentum budgets close; results converge under grid refinement.

The seed that lets chi leave the unstable point chi = 0 is small band-limited noise - a classical
proxy for vacuum/thermal fluctuations.  The run is a consistency test of the model's equations;
it is not evidence that such events occur.
"""
from __future__ import annotations

import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

from crh_common import AQUA, BLUE, INK2, ORANGE, Timer, save_json, setup_matplotlib

LAM = 1.0
W_BODY, EDGE = 30.0, 0.5            # body width and edge thickness
XMAX, SPONGE = 200.0, 50.0          # half-box and absorber thickness
M_A, K_A, ZETA_A = 1000.0, 40.0, 0.25
X_START = -60.0


def top(y, w=W_BODY, s=EDGE):
    return 0.5 * (np.tanh((y + w / 2) / s) - np.tanh((y - w / 2) / s))


def dtop(y, w=W_BODY, s=EDGE):
    return 0.5 * (np.tanh((y - w / 2) / s) ** 2 - np.tanh((y + w / 2) / s) ** 2) / s   # sech^2 = 1 - tanh^2


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * u * (10.0 - 15.0 * u + 6.0 * u * u)


def dsmoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return 30.0 * u * u * (1.0 - u) ** 2


def seed_field(x, amp=1e-8, nmodes=120, rng_seed=7):
    """Resolution-independent small seed: fixed Fourier modes with fixed random phases."""
    rng = np.random.default_rng(rng_seed)
    ks = 2 * np.pi * np.arange(1, nmodes + 1) / (2 * XMAX)
    a, ph = rng.normal(size=nmodes), rng.uniform(0, 2 * np.pi, size=nmodes)
    f = sum(a[j] * np.cos(ks[j] * x + ph[j]) for j in range(nmodes))
    return amp * f / np.sqrt(np.mean(f**2))


def critical_depth(r0, h=0.01):
    """Overlap depth at which chi = 0 first becomes unstable, for the actual smooth profiles."""
    x = np.arange(-40.0, 40.0, h) + h / 2

    def eps(depth):
        prof = r0 * top(x) * top(x - (depth - W_BODY))       # B's right edge `depth` inside A's left edge
        d = 2.0 / h**2 + 1.0 - prof
        return eigh_tridiagonal(d, -np.ones(x.size - 1) / h**2, select="i", select_range=(0, 0), eigvals_only=True)[0]

    if eps(10.0) > 0:
        return np.inf
    return brentq(eps, -3.0, 10.0, xtol=1e-6)


def simulate(r0: float, depth_max: float, dx: float = 0.1, cfl: float = 0.4,
             t_move: float = 400.0, t_hold: float = 300.0, t_wait: float = 700.0, n_samples: int = 3600):
    n = int(round(2 * XMAX / dx))
    x = -XMAX + (np.arange(n) + 0.5) * dx
    dt = cfl * dx
    t_end = 2 * t_move + t_hold + t_wait
    nsteps = int(round(t_end / dt))
    dt = t_end / nsteps
    x_end = depth_max - W_BODY                              # X_B at closest approach (X_A ~ 0)

    def XB(t):
        return X_START + (x_end - X_START) * (smoothstep(t / t_move) - smoothstep((t - t_move - t_hold) / t_move))

    def VB(t):
        return (x_end - X_START) * (dsmoothstep(t / t_move) - dsmoothstep((t - t_move - t_hold) / t_move)) / t_move

    gam = np.where(np.abs(x) > XMAX - SPONGE, 0.5 * ((np.abs(x) - (XMAX - SPONGE)) / SPONGE) ** 2, 0.0)
    damp = np.exp(-gam * dt / 2)
    sp = gam > 0
    gamA = 2 * ZETA_A * np.sqrt(K_A / M_A)
    dampA = np.exp(-gamA * dt / 2)

    chi, pi = seed_field(x), np.zeros(n)
    XA, PA = 0.0, 0.0

    def profiles(XA, xb):
        return top(x - XA), top(x - xb), dtop(x - XA), dtop(x - xb)

    def kicks(chi, XA, t):
        nA, nB, dA, dB = profiles(XA, XB(t))
        c2 = chi * chi
        lapc = (np.roll(chi, -1) - 2 * chi + np.roll(chi, 1)) / dx**2
        fchi = lapc - (1.0 - r0 * nA * nB) * chi - LAM * chi * c2
        FA = -0.5 * r0 * dx * np.sum(c2 * dA * nB)          # gate force on body A
        FB = -0.5 * r0 * dx * np.sum(c2 * nA * dB)          # gate force on body B
        return fchi, FA, FB, nA * nB

    def field_E(chi, pi):
        d = (np.roll(chi, -1) - chi) / dx
        return dx * np.sum(0.5 * pi**2 + 0.5 * d**2 + 0.5 * chi**2 + 0.25 * LAM * chi**4)

    def field_P(chi, pi):
        return -dx * np.sum(pi * (np.roll(chi, -1) - np.roll(chi, 1)) / (2 * dx))

    fchi, FA, FB, ov = kicks(chi, XA, 0.0)
    E_sponge = P_sponge = Q_A = W_B = I_ext = 0.0           # running integrals for the budgets
    every = max(1, nsteps // n_samples)
    rec = []

    def sample(t):
        Eint = -0.5 * r0 * dx * np.sum(chi * chi * ov)
        Echi = field_E(chi, pi)
        EA = PA * PA / (2 * M_A) + 0.5 * K_A * XA * XA
        sel = ov > 1e-3
        rec.append((t, XA, XB(t), FA, FB, field_P(chi, pi), Echi, Eint, EA,
                    float(np.max(np.abs(chi[sel]))) if sel.any() else 0.0,
                    float(np.max(np.abs(chi[np.abs(x) < 80.0]))),
                    E_sponge, P_sponge, Q_A, W_B, I_ext, PA))

    sample(0.0)
    for i in range(nsteps):
        t = i * dt
        # --- half step: dissipation then kick
        if True:
            before = pi[sp].copy()
            pi *= damp
            E_sponge += 0.5 * dx * np.sum(before**2 - pi[sp] ** 2)
            P_sponge += -dx * np.sum((before - pi[sp]) * ((np.roll(chi, -1) - np.roll(chi, 1)) / (2 * dx))[sp])
            Q_A += (PA * PA) * (1 - dampA**2) / (2 * M_A)
            PA *= dampA
        pi += 0.5 * dt * fchi
        PA += 0.5 * dt * (FA - K_A * XA)
        I_ext += 0.5 * dt * (-K_A * XA - FB)                 # impulse delivered by A's spring and B's driver
        W_B += 0.5 * dt * (FB * VB(t))
        # --- drift
        chi += dt * pi
        XA += dt * PA / M_A
        # --- half step: kick then dissipation
        fchi, FA, FB, ov = kicks(chi, XA, t + dt)
        pi += 0.5 * dt * fchi
        PA += 0.5 * dt * (FA - K_A * XA)
        I_ext += 0.5 * dt * (-K_A * XA - FB)
        W_B += 0.5 * dt * (FB * VB(t + dt))
        before = pi[sp].copy()
        pi *= damp
        E_sponge += 0.5 * dx * np.sum(before**2 - pi[sp] ** 2)
        P_sponge += -dx * np.sum((before - pi[sp]) * ((np.roll(chi, -1) - np.roll(chi, 1)) / (2 * dx))[sp])
        Q_A += (PA * PA) * (1 - dampA**2) / (2 * M_A)
        PA *= dampA
        if (i + 1) % every == 0 or i == nsteps - 1:
            sample(t + dt)

    r = np.array(rec)
    keys = ("t", "XA", "XB", "FA", "FB", "Pchi", "Echi", "Eint", "EA", "chi_max_overlap", "chi_max_bodies",
            "E_sponge", "P_sponge", "Q_A", "W_B", "I_ext", "PA")
    out = {k: r[:, j] for j, k in enumerate(keys)}
    out["depth"] = out["XB"] + W_BODY - out["XA"]            # geometric overlap depth (negative = apart)
    # budgets (should be constant in time):
    #   energy:   E_chi + E_int + E_A + [sponge loss] + [heat in A] + int F_B V_B dt
    #   momentum: P_A + P_chi + [sponge loss] - int (-K_A X_A - F_B) dt     (A's damping is internal to A's anchor;
    #             it is included through the measured P_A change, see below)
    out["energy_budget"] = out["Echi"] + out["Eint"] + out["EA"] + out["E_sponge"] + out["Q_A"] + out["W_B"]
    out.update(dict(dx=dx, dt=dt, r0=r0, depth_max=depth_max, t_move=t_move, t_hold=t_hold, t_end=t_end))
    return out


def main() -> int:
    plt = setup_matplotlib()
    r0 = 5.0
    u_bulk = (r0 - 1) ** 2 / (4 * LAM)
    dc = critical_depth(r0)
    print(f"r0 = {r0}: bulk traction u = {u_bulk};  critical overlap depth for these profiles d_c = {dc:.4f}")
    summary: dict = {"r0": r0, "u_bulk": u_bulk, "critical_depth": dc,
                     "quasi_static_displacement_prediction": -u_bulk / K_A}

    with Timer("four runs at dx = 0.1"):
        base = simulate(0.0, 10.0)
        subd = simulate(0.9, 10.0)                # densities below threshold everywhere
        subs = simulate(r0, 0.8 * dc)             # dense enough, but overlap region too small
        hit = simulate(r0, 10.0)                  # the contact event

    def describe(tag, s):
        return {"run": tag, "max_abs_XA": float(np.max(np.abs(s["XA"]))),
                "max_gate_amplitude": float(np.max(s["chi_max_bodies"])),
                "max_abs_force_on_A": float(np.max(np.abs(s["FA"])))}

    runs = [describe("baseline r0=0", base), describe("sub-threshold density r0=0.9", subd),
            describe("sub-critical size (depth 0.8 d_c)", subs), describe("contact r0=5 depth 10", hit)]
    for q in runs:
        print(f"   {q['run']:36s} max|X_A| = {q['max_abs_XA']:.3e}   max|chi| = {q['max_gate_amplitude']:.3e}"
              f"   max|F_A| = {q['max_abs_force_on_A']:.3e}")
    summary["runs"] = runs

    # ---- contact run: quantitative checks
    t = hit["t"]
    hold = (t > hit["t_move"] + 0.5 * hit["t_hold"]) & (t < hit["t_move"] + hit["t_hold"])
    FA_hold, FB_hold, XA_hold = hit["FA"][hold].mean(), hit["FB"][hold].mean(), hit["XA"][hold].mean()
    print(f"   during hold:  F_A = {FA_hold:+.4f} (prediction -u = {-u_bulk:+.4f}),  F_B = {FB_hold:+.4f},"
          f"  X_A = {XA_hold:+.5f} (prediction {-u_bulk / K_A:+.5f})")
    # onset: first time the gate amplitude exceeds 1% of the bulk value, and the overlap depth then
    bulk_amp = np.sqrt((r0 - 1) / LAM)
    i_on = int(np.argmax(hit["chi_max_bodies"] > 0.01 * bulk_amp))
    i_dc = int(np.argmax(hit["depth"] > dc))
    print(f"   overlap depth crosses d_c at t = {t[i_dc]:.1f}; gate reaches 1% of bulk amplitude at t = {t[i_on]:.1f}"
          f" (depth then = {hit['depth'][i_on]:.3f})")
    # Newton's third law with the gate: F_A + F_B + dP_chi/dt = 0 (away from the absorbers)
    dP = np.gradient(hit["Pchi"] + hit["P_sponge"], t)
    third = hit["FA"] + hit["FB"] + dP
    scale = np.max(np.abs(hit["FA"]))
    third_rms = float(np.sqrt(np.mean(third**2)) / scale)
    print(f"   Newton's third law incl. gate momentum: rms(F_A + F_B + dP_chi/dt) / max|F_A| = {third_rms:.2e}")
    eb = hit["energy_budget"]
    e_scale = float(np.max(np.abs(hit["Eint"])))
    e_drift = float(np.max(np.abs(eb - eb[0])) / e_scale)
    print(f"   energy budget drift / max|E_int| = {e_drift:.2e}   (max |E_int| = {e_scale:.3f})")
    # after the event: the coupling term is identically zero once the bodies are apart, whatever chi does;
    # what lingers is free, dispersing gate radiation.  Measure how fast it leaves the site.
    t_sep = 2 * hit["t_move"] + hit["t_hold"]                # bodies fully separated from here on
    w1 = (t > t_sep + 100.0) & (t < t_sep + 200.0)
    w2 = (t > hit["t_end"] - 100.0)
    amp1, amp2 = float(np.max(hit["chi_max_bodies"][w1])), float(np.max(hit["chi_max_bodies"][w2]))
    t1, t2 = t_sep + 150.0 - (hit["t_move"] + hit["t_hold"]), hit["t_end"] - 50.0 - (hit["t_move"] + hit["t_hold"])
    decay_exp = float(np.log(amp2 / amp1) / np.log(t2 / t1))
    resid_amp = amp2
    resid_F = float(np.max(np.abs(hit["FA"][t > t_sep + 50.0])))
    E_rad = float(hit["E_sponge"][-1] + hit["Echi"][-1])
    print(f"   after retraction: max|F_A| = {resid_F:.2e};  lingering free gate field near the site:"
          f" {amp1:.2e} -> {amp2:.2e} (bulk value was {bulk_amp:.2f}), local decay ~ t^{decay_exp:.2f}")
    print(f"   energy radiated into free gate quanta (absorbed + still in box) = {E_rad:.4e}"
          f" = {E_rad / e_scale:.2e} of the peak gate energy")
    summary["contact"] = {"F_A_hold": float(FA_hold), "F_B_hold": float(FB_hold), "X_A_hold": float(XA_hold),
                          "t_cross_dc": float(t[i_dc]), "t_gate_on": float(t[i_on]),
                          "depth_at_gate_on": float(hit["depth"][i_on]), "third_law_rms_rel": third_rms,
                          "energy_budget_drift_rel": e_drift, "peak_gate_energy": e_scale,
                          "residual_gate_amplitude_early": amp1, "residual_gate_amplitude_late": amp2,
                          "residual_decay_exponent": decay_exp, "residual_force": resid_F,
                          "radiated_energy": E_rad, "radiated_fraction": E_rad / e_scale}

    # ---- convergence
    print("   grid refinement of the contact run:")
    conv = []
    with Timer("convergence runs"):
        for dx in (0.2, 0.1, 0.05):
            s = hit if dx == 0.1 else simulate(r0, 10.0, dx=dx)
            tt = s["t"]
            h2 = (tt > s["t_move"] + 0.5 * s["t_hold"]) & (tt < s["t_move"] + s["t_hold"])
            conv.append({"dx": dx, "F_A_hold": float(s["FA"][h2].mean()), "X_A_hold": float(s["XA"][h2].mean()),
                         "min_X_A": float(s["XA"].min()),
                         "t_gate_on": float(tt[int(np.argmax(s['chi_max_bodies'] > 0.01 * bulk_amp))])})
            print(f"      dx={dx:5.2f}: F_A(hold) = {conv[-1]['F_A_hold']:+.5f}   X_A(hold) = {conv[-1]['X_A_hold']:+.6f}"
                  f"   min X_A = {conv[-1]['min_X_A']:+.6f}   t_on = {conv[-1]['t_gate_on']:.1f}")
    summary["convergence"] = conv

    # ---- figure: four stacked panels sharing the time axis (one quantity per axis)
    fig, axs = plt.subplots(4, 1, figsize=(8.6, 10.2), sharex=True)
    ax = axs[0]
    ax.plot(t, hit["depth"], color=BLUE)
    ax.axhline(dc, color=ORANGE, lw=1.4, ls=(0, (6, 3)))
    ax.text(t[-1], dc + 1.2, f"critical depth $d_c$ = {dc:.2f}", ha="right", fontsize=8, color=INK2)
    ax.axhline(0, color=INK2, lw=0.6)
    ax.set_ylim(-32, 14); ax.set_ylabel("overlap depth  [1/$\\mu$]")
    ax.set_title("A contact event: the B body approaches, overlaps the A body, holds, and retracts")

    ax = axs[1]
    ax.plot(t, hit["chi_max_bodies"], color=BLUE)
    ax.axhline(bulk_amp, color=INK2, lw=0.6)
    ax.text(t[-1], bulk_amp * 1.03, "bulk open-gate value", ha="right", fontsize=8, color=INK2)
    ax.set_ylabel("gate amplitude  max|$\\chi$|")

    ax = axs[2]
    ax.plot(t, hit["FA"] / u_bulk, color=BLUE, label="gate force on A (skin)")
    ax.plot(t, hit["FB"] / u_bulk, color=ORANGE, ls=(0, (6, 3)), label="gate force on B (hand)")
    ax.plot(t, (hit["FA"] + hit["FB"]) / u_bulk, color=AQUA, ls=":", lw=2.4, label="sum = $-$d$P_\\chi$/dt")
    ax.set_ylim(-2.2, 3.4)
    ax.set_ylabel("force / bulk traction u"); ax.legend(loc="upper right", ncol=1)

    ax = axs[3]
    ax.plot(t, hit["XA"], color=BLUE, label="contact (r$_0$ = 5, depth 10)")
    ax.plot(t, subs["XA"], color=ORANGE, ls=(0, (6, 3)), label="overlap too small (0.8 $d_c$)")
    ax.plot(t, subd["XA"], color=AQUA, ls=":", lw=2.4, label="densities too low (r$_0$ = 0.9)")
    ax.axhline(-u_bulk / K_A, color=INK2, lw=0.6)
    ax.text(t[-1], -u_bulk / K_A + 0.004, "quasi-static prediction  $-u/K_A$", ha="right", fontsize=8, color=INK2)
    ax.set_ylabel("displacement of A,  $X_A$"); ax.set_xlabel("time  [1/$\\mu$]")
    ax.set_ylim(-0.16, 0.13)
    ax.legend(loc="upper right")
    fig.align_ylabels(axs)
    fig.savefig("results/exp4_contact_event.png")
    plt.close(fig)

    save_json("exp4_contact_event.json", summary)
    ok = (runs[0]["max_abs_XA"] == 0.0 and runs[1]["max_abs_XA"] < 1e-12 and runs[2]["max_abs_XA"] < 1e-12
          and abs(FA_hold / (-u_bulk) - 1) < 0.02 and abs(XA_hold / (-u_bulk / K_A) - 1) < 0.02
          and third_rms < 2e-2 and e_drift < 1e-2 and resid_F < 1e-12 and amp2 < amp1)
    print("RESULT:", "consistent with Theorems 2-3 and the conservation laws" if ok else "CHECK FAILED - inspect numbers")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
