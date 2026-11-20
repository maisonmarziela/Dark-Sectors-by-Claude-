"""Experiment 7 - Monte-Carlo test of the cross-force positivity bound (manuscript Theorem 1).

Claim.  Let sectors A and B couple to any number of mediators of the same exchange sign
(e.g. several scalars of arbitrary masses) through FACTORISED couplings g_X^i (X = A, B).
Then for two bodies with non-negative charge densities separated by a plane,

        |F_AB|  <=  sqrt( F_AA * F_BB )           (and the same for interaction energies),

where F_AA is the mediator force the same two bodies would feel if both carried sector-A
charges, and F_BB likewise for sector B.  Consequently a strong cross-sector force together with
an experimentally small same-sector "fifth force" F_AA forces a huge B-B self-force.

Loopholes exhibited here:
  * exchange channels of opposite sign (a scalar and a vector, degenerate and tuned) violate it;
  * non-factorised "product" portals (chi coupled to O_A*O_B) are outside its hypotheses - they
    generate no A-A force at all at tree level.

This is a numerical sanity check of an inequality that is proven analytically in the manuscript
(Cauchy-Schwarz with a positive weight); a Monte-Carlo scan cannot prove it, only fail to break it.
"""
from __future__ import annotations

import numpy as np

from crh_common import save_json


def yukawa_energy_weights(m, d):
    """sum over point pairs of exp(-m d)/(4 pi d): positive weights w_i for each mediator."""
    return np.array([np.sum(np.exp(-mi * d) / (4 * np.pi * d)) for mi in m])


def yukawa_force_weights(m, d, dz):
    """normal (z) component of the pair forces, summed; positive when the bodies are separated by a z-plane."""
    return np.array([np.sum((1 + mi * d) * np.exp(-mi * d) / (4 * np.pi * d**3) * dz) for mi in m])


def main() -> int:
    rng = np.random.default_rng(20261110)
    n_trials = 20000
    worst_E, worst_F, viol = np.inf, np.inf, 0
    for _ in range(n_trials):
        nmed = rng.integers(1, 7)
        m = 10 ** rng.uniform(-2, 1.5, size=nmed)                 # mediator masses
        gA, gB = rng.normal(size=nmed), rng.normal(size=nmed)     # factorised couplings (any signs)
        # two random blobs of points on either side of the plane z = 0
        n1, n2 = rng.integers(1, 12), rng.integers(1, 12)
        gap = 10 ** rng.uniform(-1.5, 1)
        p1 = np.c_[rng.normal(size=(n1, 2)), -gap / 2 - rng.exponential(1.0, n1)]
        p2 = np.c_[rng.normal(size=(n2, 2)), +gap / 2 + rng.exponential(1.0, n2)]
        q1, q2 = rng.uniform(0.1, 1, n1), rng.uniform(0.1, 1, n2)  # non-negative "charges" (masses)
        diff = p2[None, :, :] - p1[:, None, :]
        d = np.linalg.norm(diff, axis=2)
        qq = q1[:, None] * q2[None, :]
        wE = np.array([np.sum(qq * np.exp(-mi * d) / (4 * np.pi * d)) for mi in m])
        wF = np.array([np.sum(qq * (1 + mi * d) * np.exp(-mi * d) / (4 * np.pi * d**3) * diff[:, :, 2]) for mi in m])
        for w, kind in ((wE, "E"), (wF, "F")):
            AB, AA, BB = np.sum(gA * gB * w), np.sum(gA * gA * w), np.sum(gB * gB * w)
            margin = (AA * BB - AB * AB) / (AA * BB)
            if kind == "E":
                worst_E = min(worst_E, margin)
            else:
                worst_F = min(worst_F, margin)
            if margin < -1e-12:
                viol += 1
    print(f"same-sign mediators, {n_trials} random configurations: violations = {viol}")
    print(f"   smallest relative margin 1 - U_AB^2/(U_AA U_BB): energy {worst_E:.3e}, normal force {worst_F:.3e}")

    # ---- loophole: opposite-sign channels (scalar attracts, vector repels), degenerate masses, tuned couplings
    a, b, Y = 1.0, 1.0, 1.0                                       # Y = common Yukawa weight
    U_AA = (-a * a + a * a) * Y            # scalar (-) + vector (+)
    U_BB = (-b * b + (-b) * (-b)) * Y
    U_AB = (-a * b + a * (-b)) * Y
    print(f"mixed-sign counterexample (degenerate scalar+vector): U_AA = {U_AA}, U_BB = {U_BB}, U_AB = {U_AB}"
          "  -> bound violated (requires exact degeneracy and tuned charges)")
    # how fast the loophole closes when the degeneracy is broken: masses m and m(1+delta), at distance r = 1/m
    rows = []
    for delta in (0.0, 1e-3, 1e-2, 1e-1):
        ws, wv = np.exp(-1.0), np.exp(-(1 + delta))
        AA, BB, AB = -a * a * ws + a * a * wv, -b * b * ws + b * b * wv, -a * b * ws - a * b * wv
        rows.append({"delta": delta, "U_AA_over_U_AB": AA / AB})
        print(f"   mass splitting delta = {delta:g}:  U_AA / U_AB = {AA / AB:+.3e}")

    save_json("exp7_positivity_bound.json", {"n_trials": n_trials, "violations": viol,
                                             "min_margin_energy": worst_E, "min_margin_force": worst_F,
                                             "mixed_sign_counterexample": {"U_AA": U_AA, "U_BB": U_BB, "U_AB": U_AB},
                                             "degeneracy_breaking": rows})
    ok = viol == 0
    print("RESULT:", "no violation found for same-sign factorised exchange" if ok else "VIOLATION FOUND - theorem wrong?")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
