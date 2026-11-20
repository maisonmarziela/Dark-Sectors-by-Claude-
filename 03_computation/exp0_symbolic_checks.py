"""Experiment 0 - computer-algebra verification of the analytic identities used in the manuscript.

Each check prints PASS/FAIL.  These are *independent re-derivations* of formulas
that were first obtained by hand; they guard against algebra slips, nothing more.

Checks
  S1  sector balance laws:  d_mu T_A^{mu nu} = -F O_B d^nu O_A   (energy and momentum)
  S2  total energy-momentum conservation with a dynamical gate
  S3  non-conservation formula for a prescribed (non-dynamical) gate
  S4  slab and ball threshold formulas solve the matching conditions
  S5  bulk gate energy densities (even gate and odd gate)
  S6  bimetric mass eigenstates, the 4/3 factor, and the cross-sector potential
  S7  the positivity (Cauchy-Schwarz) bound holds for the bimetric potentials
"""
from __future__ import annotations

import sympy as sp

from crh_common import save_json

results: dict[str, bool] = {}


def report(key: str, ok: bool, note: str = "") -> None:
    results[key] = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {key}  {note}")


def main() -> int:
    t, x = sp.symbols("t x", real=True)
    fA, fB, ch = (sp.Function(n)(t, x) for n in ("phi_A", "phi_B", "chi"))
    VA, VB, VC, OA, OB, F = (sp.Function(n) for n in ("V_A", "V_B", "V_chi", "O_A", "O_B", "F"))

    # Lagrangian density (signature +,-):  L = sum 1/2(d phi)^2 - V  -  F(chi) O_A(phi_A) O_B(phi_B)
    Lint = -F(ch) * OA(fA) * OB(fB)

    def eom_rhs(f, V):
        """phi_tt = phi_xx - V'(phi) + d L_int / d phi"""
        return sp.diff(f, x, 2) - sp.diff(V(f), f) + sp.diff(Lint, f)

    rhs = {sp.Derivative(f, (t, 2)): eom_rhs(f, V) for f, V in ((fA, VA), (fB, VB), (ch, VC))}

    def on_shell(expr):
        return sp.simplify(sp.expand(expr.doit().subs(rhs).doit()))

    def dens(f, V):
        e = sp.Rational(1, 2) * sp.diff(f, t) ** 2 + sp.Rational(1, 2) * sp.diff(f, x) ** 2 + V(f)  # T^00
        S = -sp.diff(f, t) * sp.diff(f, x)                                                       # T^0x = T^x0
        tau = sp.Rational(1, 2) * sp.diff(f, t) ** 2 + sp.Rational(1, 2) * sp.diff(f, x) ** 2 - V(f)  # T^xx
        return e, S, tau

    eA, SA, tA = dens(fA, VA)
    eB, SB, tB = dens(fB, VB)
    eC, SC, tC = dens(ch, VC)

    print("S1  sector balance laws")
    # energy:    d_t e_A + d_x S_A = -F O_B d_t O_A
    report("S1a energy balance of sector A",
           on_shell(sp.diff(eA, t) + sp.diff(SA, x) + F(ch) * OB(fB) * sp.diff(OA(fA), t)) == 0)
    # momentum:  d_t p_A + d_x tau_A = +F O_B d_x O_A      (p_A = T^0x = S_A)
    report("S1b momentum balance of sector A",
           on_shell(sp.diff(SA, t) + sp.diff(tA, x) - F(ch) * OB(fB) * sp.diff(OA(fA), x)) == 0)
    report("S1c momentum balance of the gate",
           on_shell(sp.diff(SC, t) + sp.diff(tC, x) - OA(fA) * OB(fB) * sp.diff(F(ch), x)) == 0)

    print("S2  total conservation (dynamical gate)")
    e_int = F(ch) * OA(fA) * OB(fB)          # T_int^{00} = +F O_A O_B ;  T_int^{xx} = -F O_A O_B
    report("S2a total energy", on_shell(sp.diff(eA + eB + eC + e_int, t) + sp.diff(SA + SB + SC, x)) == 0)
    report("S2b total momentum", on_shell(sp.diff(SA + SB + SC, t) + sp.diff(tA + tB + tC - e_int, x)) == 0)

    print("S3  prescribed gate f(t,x): what fails to be conserved")
    f = sp.Function("f")(t, x)
    Lint_p = -f * OA(fA) * OB(fB)
    rhs_p = {sp.Derivative(g, (t, 2)): sp.diff(g, x, 2) - sp.diff(V(g), g) + sp.diff(Lint_p, g)
             for g, V in ((fA, VA), (fB, VB))}

    def on_shell_p(expr):
        return sp.simplify(sp.expand(expr.doit().subs(rhs_p).doit()))

    e_int_p = f * OA(fA) * OB(fB)
    # d_t(e_A+e_B+e_int) + d_x(S_A+S_B) = +(d_t f) O_A O_B
    report("S3a energy source = +(d_t f) O_A O_B",
           on_shell_p(sp.diff(eA + eB + e_int_p, t) + sp.diff(SA + SB, x) - sp.diff(f, t) * OA(fA) * OB(fB)) == 0)
    # d_t(p_A+p_B) + d_x(tau_A+tau_B - e_int) = -(d_x f) O_A O_B
    report("S3b momentum source = -(d_x f) O_A O_B",
           on_shell_p(sp.diff(SA + SB, t) + sp.diff(tA + tB - e_int_p, x) + sp.diff(f, x) * OA(fA) * OB(fB)) == 0)

    print("S4  finite-size thresholds")
    mu, r, lam = sp.symbols("mu r lambda", positive=True)
    s = sp.sqrt(r - 1)                      # requires r > 1
    k0 = mu * s
    Lc = 2 * sp.atan(1 / s) / k0
    Rc = (sp.pi - sp.atan(s)) / k0
    num = {mu: sp.Rational(7, 5), r: sp.Rational(23, 5)}
    slab = sp.simplify(k0 * sp.tan(k0 * Lc / 2) - mu)
    ball = (k0 * sp.cot(k0 * Rc) + mu)
    report("S4a slab  k0 tan(k0 Lc/2) = mu", slab == 0 or abs(sp.N(slab.subs(num))) < 1e-12)
    report("S4b ball  k0 cot(k0 Rc) = -mu", sp.simplify(ball) == 0 or abs(sp.N(ball.subs(num))) < 1e-12)
    # limits quoted in the text
    report("S4c slab  Lc -> pi/(mu sqrt(r-1)) as r->1+",
           sp.limit(Lc * k0, r, 1, "+") == sp.pi)
    report("S4d slab  Lc ~ 2/(mu (r-1)) as r->oo", sp.limit(Lc * mu * (r - 1), r, sp.oo) == 2)
    report("S4e ball  (r-1) mu^2 Rc^2 > pi^2/4 for all r>1",
           all(sp.N(((r - 1) * mu**2 * Rc**2).subs({mu: 1, r: rv})) > sp.N(sp.pi**2 / 4)
               for rv in (sp.Rational(101, 100), 2, 10, 1000, 10**6)))

    print("S5  bulk gate energy densities")
    c, sgm, nA, nB, M = sp.symbols("chi s n_A n_B M", positive=True)
    Veven = sp.Rational(1, 2) * (mu**2 - sgm) * c**2 + lam * c**4 / 4
    c2 = sp.solve(sp.diff(Veven, c), c**2)
    Vmin = sp.simplify(Veven.subs(c**2, (sgm - mu**2) / lam).subs(c**4, ((sgm - mu**2) / lam) ** 2))
    report("S5a even gate  V_min = -(s-mu^2)^2/(4 lambda)",
           sp.simplify(Vmin + (sgm - mu**2) ** 2 / (4 * lam)) == 0, f"(stationary chi^2 = {c2})")
    cc = sp.symbols("chi_", real=True)
    Vodd = sp.Rational(1, 2) * mu**2 * cc**2 + cc * nA * nB / M**3
    c_star = sp.solve(sp.diff(Vodd, cc), cc)[0]
    report("S5b odd gate   V_min = -(n_A n_B)^2/(2 M^6 mu^2)",
           sp.simplify(Vodd.subs(cc, c_star) + (nA * nB) ** 2 / (2 * M**6 * mu**2)) == 0)

    print("S6  bimetric bookkeeping (linearised, proportional backgrounds)")
    Mg, Mf, TA, TB, u, v = sp.symbols("M_g M_f T_A T_B u v", positive=True)
    Meff = sp.sqrt(Mg**2 + Mf**2)
    h = (Mg * u - Mf * v) / Meff            # perturbation of the A metric, canonically normalised
    l = (Mf * u + Mg * v) / Meff            # perturbation of the B metric
    src = sp.expand(h * TA / Mg + l * TB / Mf)
    cu, cv = sp.simplify(src.coeff(u) * Meff), sp.simplify(src.coeff(v) * Meff)
    alpha = Mf / Mg
    report("S6a massless mode couples to T_A + T_B", sp.simplify(cu - (TA + TB)) == 0)
    report("S6b massive mode couples to -alpha T_A + T_B/alpha", sp.simplify(cv - (-alpha * TA + TB / alpha)) == 0)
    # tensor structure for static sources T^{mu nu} = diag(m,0,0,0):
    m1, m2 = sp.symbols("m_1 m_2", positive=True)
    massless = m1 * m2 * (1 - sp.Rational(1, 2))     # T.T' - 1/2 T T'
    massive = m1 * m2 * (1 - sp.Rational(1, 3))      # T.T' - 1/3 T T'
    report("S6c massive/massless static weight = 4/3", sp.simplify(massive / massless) == sp.Rational(4, 3))

    print("S7  positivity bound for the bimetric potentials")
    y, a = sp.symbols("y alpha", positive=True)       # y = exp(-m r) in (0,1]
    VAA = 1 + sp.Rational(4, 3) * a**2 * y
    VBB = 1 + sp.Rational(4, 3) * y / a**2
    VAB = 1 - sp.Rational(4, 3) * y
    gap = sp.simplify(VAA * VBB - VAB**2)             # should be >= 0
    # gap = (4/3) y (a^2 + a^-2 + 2) = (4/3) y (a + 1/a)^2
    report("S7  V_AA V_BB - V_AB^2 = (4/3) y (alpha + 1/alpha)^2 >= 0",
           sp.simplify(gap - sp.Rational(4, 3) * y * (a + 1 / a) ** 2) == 0)

    ok = all(results.values())
    save_json("exp0_symbolic_checks.json", {"all_pass": ok, "checks": results})
    print(f"\n{sum(results.values())}/{len(results)} symbolic checks passed")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
