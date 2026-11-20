"""Experiment 6 - the numbers: how strong must a cross-sector coupling be to be FELT?

Pure arithmetic with physical constants (SI internally; natural-unit conversions are explicit).
Every number quoted in the manuscript's phenomenology sections is produced here, so that a
reader can change an assumption (e.g. the touch threshold) and re-derive everything.

These are order-of-magnitude estimates.  Inputs that are assumptions rather than measurements
are collected in ASSUMPTIONS and are flagged in the printed output.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import constants as C

from crh_common import RESULTS, save_json

# ------------------------------------------------------------------ constants
hbar, c, e, kB, G_N, m_u = C.hbar, C.c, C.e, C.k, C.G, C.atomic_mass
eV, GeV = e, 1e9 * e
hbarc = hbar * c                                   # J m
HBARC_eV_m = hbarc / eV                            # 1.973e-7 eV m
G_F = C.physical_constants["Fermi coupling constant"][0]          # GeV^-2
G_F_SI = G_F / GeV**2 * hbarc**3                   # J m^3   (contact-interaction strength)
M_PL_RED = np.sqrt(hbar * c / (8 * np.pi * G_N)) * c**2 / GeV     # reduced Planck mass, GeV
M_EARTH, R_EARTH, AU, KPC = 5.9722e24, 6.371e6, 1.495978707e11, 3.0857e19
H0 = 67.4e3 / 3.0857e22                            # s^-1

ASSUMPTIONS = {
    "P_touch_fiducial_Pa": 100.0,       # ~ weight of a 1 g object on 1 cm^2; clearly perceptible (assumption)
    "P_touch_optimistic_Pa": 1.0,       # best-case dynamic (vibratory) sensitivity (assumption, not verified)
    "P_touch_firm_Pa": 1.0e4,           # a firm touch, ~1 N on 1 cm^2
    "contact_area_m2": 1.0e-4,
    "tissue_density_kg_m3": 1000.0,
    "air_density_kg_m3": 1.2,
    "tissue_shear_stiffness_Pa": 5.0e4, # soft-tissue elastic modulus scale (assumption)
    "T_K": 310.0,
    "alpha_AA_max": 1.0e-3,             # assumed bound on a new Yukawa force between ordinary bodies at cm-m range
    "hidden_mass_fraction_max": 3.8e-3, # Ignatiev & Volkas 2000 (PREM-based bound)
    "kinetic_mixing_max": 5.8e-8,       # Vigo et al. 2020 (massless mirror photon; arXiv abstract value)
    "higgs_invisible_BR_max": 0.107,    # ATLAS 2023
    "higgs_width_SM_MeV": 4.1,
    "f_N": 0.30,                        # Higgs-nucleon form factor (typical value)
    "gate_threshold_theta": 0.03,       # even gate: threshold density product / (water density)^2
    "gate_mass_eV": 2.0e-4,             # benchmark gate mass (Compton wavelength ~ 1 mm)
    "touch_duration_s": 1.0e-2,
}
A = ASSUMPTIONS


def eV4_from_Pa(P):          # energy density J/m^3 -> eV^4 (natural units)
    return P / eV * HBARC_eV_m**3


def main() -> int:
    out: dict = {"assumptions": A}
    P = A["P_touch_fiducial_Pa"]
    n_w = A["tissue_density_kg_m3"] / m_u                       # nucleons per m^3
    n_w_nat = n_w * HBARC_eV_m**3                               # eV^3

    def line(label, value, unit="", note=""):
        print(f"  {label:<66s} {value:>12.4g} {unit:<10s} {note}")

    # ============================================================ 1. what "touch" requires
    print("\n[1] What counts as touch (assumptions flagged *)")
    sw = 0.07e-3 * C.g
    line("Semmes-Weinstein 2.83 monofilament force (clinical 'normal')", sw * 1e3, "mN")
    line("* fiducial perceptible traction P_touch", P, "Pa", "(~1 g weight on 1 cm^2)")
    line("  corresponding force on 1 cm^2", P * A["contact_area_m2"] * 1e3, "mN")
    delta = P * 5e-3 / A["tissue_shear_stiffness_Pa"]
    line("* skin displacement ~ P a / E  (a = 5 mm, E = 50 kPa)", delta * 1e6, "micron")
    line("  impulse for a 10 ms event on 1 cm^2", P * A["contact_area_m2"] * A["touch_duration_s"], "N s")
    out["touch"] = {"SW_force_N": sw, "P_touch": P, "force_N": P * A["contact_area_m2"], "skin_displacement_m": delta}

    # ============================================================ 2. contact (mean-field) route
    print("\n[2] Contact route: coherent mean-field traction  P = G n_A n_B  (both bodies at water density)")
    P_weak = G_F_SI * n_w**2
    line("nucleon number density of water-density matter", n_w, "m^-3")
    line("Fermi constant as a contact strength", G_F_SI, "J m^3")
    line("traction from a WEAK-strength contact coupling (G = G_F)", P_weak, "Pa")
    rows = []
    for tag, Pt in (("optimistic", A["P_touch_optimistic_Pa"]), ("fiducial", P), ("firm", A["P_touch_firm_Pa"])):
        ratio = Pt / P_weak
        Lam = (ratio * G_F) ** -0.5
        rows.append({"case": tag, "P_Pa": Pt, "G_over_GF": ratio, "Lambda_GeV": Lam, "U_per_nucleon_eV": Pt / n_w / eV})
        line(f"required G / G_F for P = {Pt:g} Pa ({tag})", ratio, "", f"<-> contact scale {Lam:.2f} GeV")
    line("mean-field potential per nucleon at fiducial P", P / n_w / eV, "eV", "(<< thermal 0.027 eV: matter not disrupted)")
    line("hearing threshold 20 microPa  ->  G / G_F", 2e-5 / P_weak, "", "(pressure across the ear, audio band)")
    line("1 fN force sensor on 1 cm^2    ->  G / G_F", 1e-15 / A["contact_area_m2"] / P_weak, "")
    out["contact"] = {"n_w": n_w, "G_F_SI": G_F_SI, "P_weak_Pa": P_weak, "rows": rows}
    G_touch_GeV = P / P_weak * G_F                              # GeV^-2
    G_touch_SI = P / n_w**2

    # ============================================================ 3. what known portals can deliver
    print("\n[3] Maximum traction available from the standard portals (neutral, unmagnetised bodies)")
    g_hNN = A["f_N"] * 0.939 / 246.22
    gam_inv = A["higgs_invisible_BR_max"] / (1 - A["higgs_invisible_BR_max"]) * A["higgs_width_SM_MeV"] * 1e-3
    g_light = np.sqrt(8 * np.pi * gam_inv / 125.25)
    G_h_light = g_hNN * g_light / 125.25**2
    G_h_heavy = g_hNN * 1.0 / 125.25**2
    P_h_light = G_h_light / G_F * P_weak
    P_h_heavy = G_h_heavy / G_F * P_weak / 100.0                # 100 GeV particles at water MASS density
    line("weak-scale mediator (Z-like), G <= G_F", P_weak, "Pa")
    line("Higgs portal, light B particle (coupling limited by H->inv)", P_h_light, "Pa", f"(g_B < {g_light:.3g})")
    line("Higgs portal, 100 GeV B particle, g_B = 1", P_h_heavy, "Pa")
    line("photon kinetic mixing, neutral bodies, first order in epsilon", 0.0, "Pa", "(vanishes: see exp8)")
    best = max(P_weak, P_h_light, P_h_heavy)
    line("shortfall of the best standard portal vs fiducial touch", P / best, "x")
    line("shortfall vs optimistic touch", A["P_touch_optimistic_Pa"] / best, "x")
    out["portals"] = {"P_weak": P_weak, "P_higgs_light": P_h_light, "P_higgs_heavy": P_h_heavy, "g_B_light_max": g_light,
                      "shortfall_fiducial": P / best, "shortfall_optimistic": A["P_touch_optimistic_Pa"] / best}

    # ============================================================ 4. thermal contact implied by a touch-strength coupling
    print("\n[4] Thermal contact implied by a contact coupling of touch strength (order of magnitude)")
    T = A["T_K"]
    mu_N = 0.5 * m_u
    sigma_NN = mu_N**2 * G_touch_SI**2 / (np.pi * hbar**4)       # Born, contact potential
    v_NN = np.sqrt(8 * kB * T / (np.pi * mu_N))
    h_lo = n_w**2 * sigma_NN * v_NN * kB                         # W m^-3 K^-1   (nucleon-level, incoherent: floor)
    # nucleus-level (A=16 on A=16): coherent over each nucleus; Born would give sigma ~ (A_A A_B)^2 (mu/mu_N)^2 sigma_NN,
    # but the potential is then non-perturbative, so cap at a geometric (hard-sphere) cross-section.
    Anuc = 16
    mu_nuc = 0.5 * Anuc * m_u
    sigma_born = (Anuc * Anuc) ** 2 * (mu_nuc / mu_N) ** 2 * sigma_NN
    R_nuc = 1.2e-15 * Anuc ** (1 / 3)
    sigma_geo = 4 * np.pi * (2 * R_nuc) ** 2
    sigma_nuc = min(sigma_born, sigma_geo)
    v_nuc = np.sqrt(8 * kB * T / (np.pi * mu_nuc))
    h_hi = (n_w / Anuc) ** 2 * sigma_nuc * v_nuc * kB
    Cv = 4.18e6                                                  # J m^-3 K^-1 (water)
    line("nucleon-nucleon cross-section at G_touch (Born)", sigma_NN * 1e4, "cm^2")
    line("nucleus-nucleus (A=16) cross-section, Born estimate", sigma_born * 1e4, "cm^2")
    line("   ... capped at geometric value", sigma_geo * 1e4, "cm^2")
    line("volumetric heat-exchange coefficient, incoherent floor", h_lo * 1e-6, "W/cm^3/K")
    line("volumetric heat-exchange coefficient, nucleus-coherent", h_hi * 1e-6, "W/cm^3/K")
    line("thermal equilibration time of overlapping bodies (floor)", Cv / h_lo, "s")
    line("thermal equilibration time (nucleus-coherent)", Cv / h_hi, "s")
    line("always-on G allowed if co-located bodies must stay thermally", 0, "", "")
    G_iso = G_touch_GeV / G_F * np.sqrt((Cv / h_lo) / (1e10 * 3.156e7))
    line("   isolated for 10 Gyr (incoherent estimate): G / G_F <", G_iso, "")
    out["thermal"] = {"sigma_NN_m2": sigma_NN, "sigma_nuc_m2": sigma_nuc, "h_floor_W_m3_K": h_lo, "h_coherent_W_m3_K": h_hi,
                      "t_eq_floor_s": Cv / h_lo, "t_eq_coherent_s": Cv / h_hi, "G_isolation_over_GF": G_iso}

    # ============================================================ 5. long-range mediator route and the positivity bound
    print("\n[5] Long-range mediator route (two 0.1 kg bodies, 5 cm apart) and the positivity bound")
    F_grav = G_N * 0.1 * 0.1 / 0.05**2
    F_touch = P * A["contact_area_m2"]
    a_cross = F_touch / F_grav
    a_BB = a_cross**2 / A["alpha_AA_max"]
    lam_range = 0.05
    self_pot = 4 * np.pi * a_BB * G_N * A["tissue_density_kg_m3"] * lam_range**2      # J/kg, uniform medium, Yukawa range
    line("Newtonian gravity between the two bodies", F_grav, "N")
    line("required cross-sector strength / gravity", a_cross, "")
    line("* assumed bound on A-A fifth force / gravity", A["alpha_AA_max"], "")
    line("positivity bound => B-B force / gravity  >=", a_BB, "")
    line("   i.e. B-B force between the same two bodies >=", a_BB * F_grav, "N")
    line("   B self-binding per unit mass (range 5 cm) >=", self_pot, "J/kg", "(chemical binding ~ 1e6-1e7 J/kg)")
    line("   same, per nucleon", self_pot * m_u / eV, "eV")
    out["long_range"] = {"F_grav_N": F_grav, "alpha_cross": a_cross, "alpha_BB_min": a_BB, "F_BB_min_N": a_BB * F_grav,
                         "self_binding_J_per_kg": self_pot}

    # ============================================================ 6. gravity: how much hidden matter can share the Earth?
    print("\n[6] Shared gravity: hidden mass co-located with the Earth")
    rho_E = M_EARTH / (4 / 3 * np.pi * R_EARTH**3)
    rho_B = A["hidden_mass_fraction_max"] * rho_E
    line("mean density of the Earth", rho_E, "kg/m^3")
    line("max mean density of a co-located B world filling R_Earth", rho_B, "kg/m^3", "(air at sea level: 1.2)")
    line("   as a fraction of water density", rho_B / 1000.0, "")
    p_c = rho_B * 9.8 * R_EARTH                                  # crude support pressure scale
    line("   pressure scale needed to hold it up against Earth's gravity", p_c, "Pa")
    out["gravity"] = {"rho_earth": rho_E, "rho_B_max": rho_B, "support_pressure_Pa": p_c}

    # ============================================================ 7. even ("threshold") gate benchmark
    print("\n[7] Even (threshold) gate  L = 1/2 g chi^2 n_A n_B,  g = 1/M^4  - benchmark parameters")
    theta, mu = A["gate_threshold_theta"], A["gate_mass_eV"]
    r_ff = 1.0 / theta
    r_air = (A["air_density_kg_m3"] / A["tissue_density_kg_m3"]) / theta
    M4 = theta * n_w_nat**2 / mu**2
    M = M4**0.25
    P_nat = eV4_from_Pa(P)
    lam = mu**4 * (r_ff - 1) ** 2 / (4 * P_nat)
    chi_on = mu * np.sqrt((r_ff - 1) / lam)
    compton = HBARC_eV_m / mu
    Rc = (np.pi - np.arctan(np.sqrt(r_ff - 1))) / np.sqrt(r_ff - 1) * compton
    line("* threshold density product / water^2 (theta)", theta, "")
    line("overlap ratio r: flesh-flesh", r_ff, "", "(gate opens)")
    line("overlap ratio r: flesh-air", r_air, "", "(< 1: gate closed)")
    line("* gate mass mu", mu, "eV", f"(Compton wavelength {compton * 1e3:.2f} mm)")
    line("critical radius of overlap region R_c", Rc * 1e3, "mm")
    line("portal scale M", M / 1e6, "MeV")
    line("quartic self-coupling lambda (from P_touch)", lam, "")
    line("open-gate field value chi_on", chi_on, "eV")
    line("gate response time hbar/mu", hbar / (mu * eV), "s")
    fit_path = RESULTS / "exp5_adiabatic_radiation.json"
    if fit_path.exists():
        fit = json.loads(fit_path.read_text(encoding="utf-8"))["fit"]
        mutau = A["touch_duration_s"] * mu * eV / hbar
        frac = fit["energy_prefactor"] * mutau ** fit["energy_exponent"]
        line("mu*tau for a 10 ms event", mutau, "")
        line("radiated fraction of gate energy (extrapolating exp5 fit)", frac, "", "(extrapolation over ~7 decades!)")
        out["radiation_extrapolation"] = {"mu_tau": mutau, "fraction": frac}
    lam_uv = 4 * np.pi * chi_on
    tuning = (M**2 / (16 * np.pi**2)) / mu**2
    line("naturalness: gate loops must be cut off below ~4 pi chi_on", lam_uv / 1e3, "keV")
    line("naturalness: (M^2/16 pi^2) / mu^2  (tuning of mu^2 if cutoff ~ M)", tuning, "")
    G_un = (M**2 / (16 * np.pi**2)) / M4 * 1e18 / G_F           # ungated loop-induced contact term, cutoff ~ M, in G_F
    line("loop-induced UNGATED contact coupling (cutoff ~ M) / G_F", G_un, "", "(vs needed-when-open ~ G_touch/G_F)")
    out["even_gate"] = {"theta": theta, "mu_eV": mu, "r_flesh_flesh": r_ff, "r_flesh_air": r_air, "M_eV": M,
                        "lambda": lam, "chi_on_eV": chi_on, "R_c_m": Rc, "compton_m": compton,
                        "Lambda_UV_max_eV": lam_uv, "tuning": tuning, "ungated_loop_G_over_GF": G_un}

    # ============================================================ 8. odd (protected) gate = density-quartic contact term
    print("\n[8] Odd (protected) gate  L = -chi J_A.J_B / M^3  ->  E = -(n_A n_B)^2 / Lambda^8")
    Lam8 = n_w_nat**4 / P_nat
    Lam_eff = Lam8**0.125
    M_odd = (Lam8 / (2 * mu**2)) ** (1 / 6)
    line("required scale Lambda (fiducial touch, water densities)", Lam_eff / 1e3, "keV")
    line("   scaling with touch threshold: Lambda ~ P^(-1/8); for 1 Pa", (n_w_nat**4 / eV4_from_Pa(1.0)) ** 0.125 / 1e3, "keV")
    line("   corresponding M for gate mass mu = 2e-4 eV", M_odd / 1e6, "MeV")
    sup_air = (A["air_density_kg_m3"] / A["tissue_density_kg_m3"]) ** 2
    rho_dm = 0.4 * GeV / c**2 * 1e6
    line("traction for flesh overlapping AIR-density matter", P * sup_air, "Pa", "(isolation by nonlinearity)")
    line("traction for flesh overlapping dark-matter-density B matter", P * (rho_dm / 1000.0) ** 2, "Pa")
    out["odd_gate"] = {"Lambda_eff_eV": Lam_eff, "M_eV_for_mu": M_odd, "air_suppression": sup_air,
                       "P_air_Pa": P * sup_air, "P_dm_density_Pa": P * (rho_dm / 1000.0) ** 2}

    # ============================================================ 9. pre-existing gate lumps: how long can they last?
    print("\n[9] A pre-existing lump of gate field of size 1 cm")
    L = 1e-2
    line("relativistic lump / collapsing bubble: lifetime ~ L/c", L / c, "s", "(nerves need >~ 1e-3 s)")
    m_min = hbar * 1e-3 / L**2 * c**2 / eV
    line("non-relativistic cloud lasting 1 ms needs particle mass m c^2 >", m_min, "eV")
    line("galactic lump crossing time at 230 km/s", L / 2.3e5, "s")
    out["lumps"] = {"t_relativistic_s": L / c, "m_min_eV": m_min, "t_crossing_s": L / 2.3e5}

    # ============================================================ 10. bimetric escape route
    print("\n[10] Bimetric gravity: strong-coupling scale Lambda_3 = (m^2 M_Pl)^(1/3) of the link field")
    brow = []
    for tag, length in (("1 AU", AU), ("1 kpc", KPC), ("Hubble radius", c / H0)):
        m_eV = HBARC_eV_m / length
        L3 = (m_eV**2 * M_PL_RED * 1e9) ** (1 / 3)
        brow.append({"compton": tag, "m_FP_eV": m_eV, "Lambda3_eV": L3, "inv_Lambda3_m": HBARC_eV_m / L3})
        line(f"graviton Compton wavelength {tag}: 1/Lambda_3 =", HBARC_eV_m / L3, "m", f"(m_FP = {m_eV:.2e} eV)")
    out["bimetric"] = brow

    # ============================================================ 11. beyond mean field: cross-sector bound states
    print("\n[11] Beyond mean field: can an ATTRACTIVE touch-strength contact coupling bind an A nucleus to a B nucleus?")
    print("     (square well of radius b, depth V0 = A_A A_B G / (4 pi b^3/3); s-wave bound state iff"
          " 2 m_r V0 b^2/hbar^2 > pi^2/4)")
    brows = []
    for tag, An in (("H - H", 1), ("O - O", 16), ("Ca - Ca", 40)):
        m_r = 0.5 * An * m_u
        b_crit = (6 / np.pi**3) * An * An * m_r * G_touch_SI / hbar**2          # bound state iff range b < b_crit
        m_med = hbarc / b_crit / eV / 1e6                                       # mediator mass with range b_crit, MeV
        Rn = 1.2e-15 * An ** (1 / 3)
        brows.append({"pair": tag, "b_crit_fm": b_crit * 1e15, "mediator_mass_MeV": m_med,
                      "bound_at_contact_range": bool(b_crit > Rn)})
        line(f"{tag}: bound state exists if interaction range b <", b_crit * 1e15, "fm",
             f"(mediator heavier than {m_med:.3g} MeV); nuclear radius {Rn * 1e15:.1f} fm")
    V_OO = 16 * G_touch_SI * 0.16e45 / eV / 1e6                                  # one nucleus fully inside the other, MeV
    line("O - O well depth for a truly point-like contact term", V_OO, "MeV", "(nuclear-scale binding)")
    line("encounter rate of an A nucleus with B nuclei (geometric, 600 m/s)",
         (n_w / 16) * 4 * np.pi * (2 * 1.2e-15 * 16 ** (1 / 3)) ** 2 * 600.0, "1/s")
    out["bound_states"] = {"rows": brows, "V_OO_contact_MeV": V_OO}

    save_json("exp6_touch_numbers.json", out)
    print("\nNumbers written to results/exp6_touch_numbers.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
