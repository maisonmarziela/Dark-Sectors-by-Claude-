# Project CRH — Computational Experiments

Nine small, self-contained Python scripts. Each one tests a specific claim in `../02_manuscript/manuscript.md`, prints what it found, writes a JSON table (and usually a figure) to `results/`, and exits with a non-zero status if one of its internal checks fails.

**These experiments test the equations against themselves.** They can reveal an algebra slip or a false theorem. They cannot tell us whether a second sector exists.

## Requirements

- Python ≥ 3.10 (developed with 3.14)
- `numpy`, `scipy`, `matplotlib`, `sympy` — see `requirements.txt` for the versions used

```
python -m venv .venv
.venv\Scripts\python -m pip install -r 03_computation\requirements.txt      # Windows
# source .venv/bin/activate && pip install -r 03_computation/requirements.txt   # Linux / macOS
```

## Running

From this directory:

```
python run_all.py            # everything, about 6 minutes on a laptop
python run_all.py --quick    # skips the two slow dynamical runs (exp4, exp5); under a minute
python exp3_static_gate_energy.py     # any script can be run on its own
```

`run_all.py` writes the complete console log to `results/run_all_log.txt`. All random seeds are fixed, so results are reproducible to floating-point round-off. Note that `exp6` reads the fit produced by `exp5`; run them in order.

## What each experiment does

| Script | Tests | Method | Runtime |
|---|---|---|---|
| `exp0_symbolic_checks.py` | The analytic identities: balance laws, total conservation, the non-conservation formulas for a prescribed gate, threshold formulas, bulk energy densities, bimetric bookkeeping | Computer algebra (sympy); 18 checks | 2 s |
| `exp1_conservation_causality.py` | Prop. 1–2 and causality | 1+1D lattice, three scalar fields, leapfrog. (a) prescribed gate pulse: measured ΔP, ΔE vs the closed-form source integrals at four resolutions; (b) dynamical gate: total E and P; (c) compactly supported gate: coupled-minus-uncoupled difference outside the light cone | 15 s |
| `exp2_gate_threshold.py` | Theorem 2 (when the gate opens) | Lowest eigenvalue of −∇² + μ²(1−r) by a tridiagonal eigen-solver, for slabs, balls and a Gaussian overlap; comparison with the analytic thresholds; check of the Sobolev sufficient condition | 3 s |
| `exp3_static_gate_energy.py` | Theorem 3 (binding energy, bulk bound, attraction) | Newton solution of the non-linear static gate equation; W(L) for a slab, W(R) for a ball; near-threshold lower bound | 6 s |
| `exp4_contact_event.py` | A complete contact event: isolation below threshold, force = bulk traction above, Newton's third law including gate momentum, energy budget, closure after separation | 1+1D gate field coupled to two rigid bodies; absorbing boundary layers with the absorbed energy and momentum tracked; four scenarios plus a three-level grid refinement | 4 min |
| `exp5_adiabatic_radiation.py` | The radiation scaling law (6.5) | Overlap ratio of a fixed slab ramped up and down over time τ; energy left in free gate quanta vs τ (8 values × 3 seeds), seed-amplitude sweep, grid check | 1.5 min |
| `exp6_touch_numbers.py` | Every physical number in the phenomenology sections | Arithmetic with CODATA constants; assumptions collected in one dictionary at the top of the file | < 1 s |
| `exp7_positivity_bound.py` | Theorem 1 | Monte-Carlo search for violations with random mediators, couplings and body shapes; explicit mixed-sign counter-example | 3 s |
| `exp8_neutral_matter_meanfield.py` | Lemma 2 (kinetic-mixing mean field cancels for neutral matter) | Real-space quadrature of the atom–atom electrostatic energy for model atoms; independent Fourier-space check | 4 s |

`crh_common.py` holds shared helpers (lattice operators, energy and momentum functionals, plot style, JSON output). `run_all.py` is the driver.

## Numerical methods and checks

- **Time stepping:** velocity-Verlet (leapfrog), second order, symplectic for the conservative parts. Energy uses the forward-difference gradient whose variation is exactly the centred Laplacian in the equations of motion, so the semi-discrete system is exactly Hamiltonian.
- **Convergence:** exp1 (four resolutions; observed order 2.0), exp2 (four grid spacings; order 2.0), exp3 (four grid spacings), exp4 (three resolutions), exp5 (three resolutions at one τ).
- **Independent cross-checks:** symbolic vs numerical conservation laws (exp0 / exp1); analytic vs eigen-solver thresholds (exp2); static variational force vs force measured in the dynamical run (exp3 / exp4); real-space vs Fourier-space potentials (exp8).
- **Dimensional checks:** exp6 works in SI units throughout and converts to natural units explicitly; the Fermi constant as a contact strength (1.436 × 10⁻⁶² J m³) reproduces the textbook value.
- **Absorbing boundaries** (exp4, exp5): a smooth damping layer; the energy and momentum it removes are accumulated and included in the budgets.

## Known limitations

1. The dynamical simulations are 1+1-dimensional. Thresholds and static energies are also computed for 3D balls, but no 3+1D evolution was done.
2. Matter is represented by rigid profiles (exp4) or prescribed overlap functions (exp5), not by deformable media.
3. The instability that opens the gate is seeded by small classical noise standing in for quantum or thermal fluctuations; results depend on its amplitude logarithmically (measured in exp5).
4. exp6 contains order-of-magnitude estimates. Inputs that are assumptions (touch threshold, tissue stiffness, the assumed fifth-force bound, the gate benchmark) are flagged in its output.
5. exp5's measured energy exponent (−1.46 ± 0.03) differs from the scaling argument (−4/3); this is reported, not explained.

## Figures

- `results/exp1_conservation_causality.png` — non-conservation with a prescribed gate; momentum balance with a dynamical gate; light-cone confinement
- `results/exp2_gate_threshold.png` — open/closed phase diagram
- `results/exp3_static_gate_energy.png` — open-gate profiles, binding energy vs bulk bound, contact force
- `results/exp4_contact_event.png` — time history of a contact event
- `results/exp5_adiabatic_radiation.png` — radiated energy and opening delay vs switching time
- `results/exp8_neutral_matter_meanfield.png` — the cancelling repulsive and attractive regions

Every figure's numbers are also in the JSON file of the same name. Colours are from a palette checked for colour-vision-deficiency separation; series are additionally distinguished by line style and by legend.
