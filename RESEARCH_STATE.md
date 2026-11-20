# RESEARCH_STATE — Project CRH

**Last updated:** 2026-11-10 (end of session 1)
**Current classification:** Interesting but incomplete
**Status:** all seven deliverables exist; all nine computational experiments pass on a clean run.

If you are resuming this work: read this file, then `07_final_assessment/final_assessment.md`, then the "Unresolved questions" list in `04_research_journal/journal.md`.

---

## 1. Completed work

| Stage | Deliverable | State |
|---|---|---|
| Literature | `01_literature_review/literature_review.md` | Done. 82/82 arXiv ids machine-verified; 20 abstracts read; 1 paper read in full via web reader |
| Model | `02_manuscript/manuscript.md` | Done. Lemmas 1–2, Propositions 1–6, Theorems 1–3, one scaling law |
| Computation | `03_computation/` (exp0–exp8) | Done. 9/9 pass; full run ≈ 6 min; log in `results/run_all_log.txt` |
| Journal | `04_research_journal/journal.md` | Done |
| Adversarial review | `05_adversarial_review/adversarial_review.md` | Done. 5 severity-A objections stand |
| Plain-English report | `06_plain_english/companion_report.md` | Done |
| Final assessment | `07_final_assessment/final_assessment.md` | Done |

## 2. Verified findings

"Verified" = proved by hand **and** checked by computer algebra and/or numerical experiment. Not reviewed by a human.

1. **Lemma 1.** Co-location needs a shared field (logic; no numerical content).
2. **Proposition 1.** Balance laws; total conservation with a dynamical gate. [S1–S2; Exp 1b: energy to 3 × 10⁻⁶]
3. **Proposition 2.** Prescribed gates violate conservation by ΔP = −∫∇f·O_A O_B, ΔE = +∫∂_t f·O_A O_B. [S3; Exp 1a, order 2]
4. **Causality** of the gated coupling. [Exp 1c, round-off]
5. **Theorem 1.** F_AB² ≤ F_AA F_BB for same-sign factorized mediators. [Exp 7; S7]
6. **Touch bound.** G ≳ 1.9 × 10⁴ G_F × (P/100 Pa) at water density. [Exp 6; depends on an assumed threshold]
7. **Lemma 2.** No first-order mean-field energy between neutral, unpolarised bodies under kinetic mixing. [Exp 8, ≤ 5 × 10⁻⁹]
8. **Theorem 2.** Exact classical isolation; thresholds L_c, R_c; Sobolev sufficient condition. [S4; Exp 2, ≤ 3 × 10⁻⁵]
9. **Theorem 3.** W ≥ 0, monotone, bulk bound, lower bound, force → u. [S5; Exp 3; Exp 4: force = u to 5 digits]
10. **Radiation is power-law** in switching time. [Exp 5: exponent −1.46 ± 0.03; scaling argument −4/3]

Estimates (order of magnitude, not verified beyond arithmetic): Corollary 1 (twin world < 21 kg/m³), Corollary 2, Proposition 5 (thermal contact), the gate benchmarks, Proposition 6's magnitudes, the bound-state criterion.

## 3. Failed or abandoned hypotheses

| Hypothesis | Why it failed |
|---|---|
| Kinetic mixing gives a contact force between neutral bodies | Mean field vanishes at first order |
| A switch function can be prescribed | Violates conservation |
| Vacuum bubble as the gate | Runs away, or lasts ~30 ps |
| Passing field lump as the gate | Needs a coincident third kind of matter |
| A light mediator gives touch cheaply | Positivity bound: enormous B–B self-force |
| Even gate gives *natural* isolation | Zero cannot be symmetry-protected; tuning ≳ 10¹² |
| Contact events are exponentially silent | Gap closes at threshold; power law |
| Gate field returns to zero afterwards | Only the coupling term does; remnant decays as a power of time |
| Lemma 2 for all neutral matter | False for oriented dipoles; restricted to unpolarised matter |
| Mean-field treatment suffices | Attractive short-range couplings can bind nuclei across sectors |

## 4. Unresolved questions (in priority order)

1. **Ultraviolet completion.** Is there any renormalizable (or at least higher-cutoff) model producing a touch-strength product portal that survives meson-decay, beam-dump, collider, stellar, supernova and BBN constraints? *Most likely point of failure.*
2. **Cross-sector bound states.** Capture rate of A nuclei by B nuclei for attractive couplings; is there an inelastic channel? Could decide the question negatively.
3. **Mitra & Foot (2003).** Read the published appendix directly. Does it omit the electron-cloud term? What is the true leading static force (pinning at O(ε), or O(ε²))?
4. **Novelty.** Systematic search (INSPIRE) for: product-of-densities scalar triggers; "tangibility" or contact-force bounds on hidden-sector matter; the multi-mediator positivity bound.
5. **Radiation exponent.** −1.46 vs −4/3. Check with linear (not smooth-step) ramps, single-mode slabs, more seeds, larger τ; then 2+1 and 3+1 dimensions.
6. **Sequestered gate.** Make the braneworld version quantitative: brane-separation modulus as gate, bulk-mediated attraction as trigger. Does locality fix the tuning? Can it reach the required strength?
7. **Bimetric window.** Graviton Compton wavelength ~1 AU: is a co-located twin world viable, and is the link field under control at room scale?
8. **Quantum onset.** Replace the classical seed by the gate field's quantum state.
9. **Touch threshold.** Obtain a sourced psychophysical threshold appropriate to a volumetric body force.
10. **Rotational locking** of gravitationally coupled co-located bodies (relevant to R7).
11. **Gate initial conditions.** Bound on a cosmological background value of the gate field.

## 5. Next actionable steps

Concrete tasks, each doable in one session:

- [ ] Fetch and read the Mitra & Foot appendix (arXiv:astro-ph/0301229) directly; redo their eq. (8)–(11) including the electron term; update manuscript §5.3 accordingly (strengthen, soften or withdraw the discrepancy claim).
- [ ] Write `exp9_capture_estimate.py`: s-wave bound-state energies for the square-well model; radiative capture rate via gate-quantum emission using the benchmark couplings.
- [ ] Extend `exp5` with a linear-ramp option and τ up to 6400; fit with a log-corrected form; report whether the exponent approaches −4/3.
- [ ] Add a 2+1D version of `exp4` (circular bodies) to check the force law and remnant decay (expect t⁻¹).
- [ ] Draft a minimal UV model: vector mediator coupled to A baryon number, with a gate-dependent coupling to a B current; list which constraints apply as a function of mediator mass.
- [ ] INSPIRE search for prior statements of the touch bound and product portals; update literature review §11.
- [ ] Verify the `[mem]`-tagged references against publisher records.

## 6. Conventions and pitfalls for whoever continues

- Signature (+,−,−,−); ħ = c = 1; `exp6` is SI internally.
- "Overlap ratio" r = g·O_A·O_B/μ². Gate opens where r > 1 *and* the region exceeds the critical size.
- `exp6` reads `results/exp5_adiabatic_radiation.json`; run `exp5` first (or `run_all.py`).
- The touch threshold (100 Pa) is an **assumption**; do not cite it as a measured value.
- Do not strengthen the wording about Mitra & Foot until step 1 above is done.
- Python environment: `.venv/` in the project root (system site-packages plus sympy).
